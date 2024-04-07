import logging
import openai
import azure.functions as func
import pyodbc
import os
import google.generativeai as gemini

#Define a global variable to hold th emessage queue. This array will change format depending on if using Gemini or OpenAI
MessageQueue = []
LLM = ""

def main(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    global LLM
    MyPrompt = ""
    SessionID = 0
    try:
        req_body = req.get_json()
        MyPrompt = req_body.get('prompt')
        SessionID = req_body.get('sessionid')
        LLM = req_body.get('LLM')
        UseQuestions = (req_body.get('UseQuestions') == "yes")
    except:
        return "Parameter Error!    Usage: {\"prompt\":\"<Prompt Text>\",\"sessionid\":<SessionID>,\"LLM\":\"GPT3.5\", \"UseQuestions\":\"yes\"}"

    try:
        Output = CallAI(MyPrompt,SessionID,UseQuestions)
        return func.HttpResponse(Output, status_code=200)
    except Exception as e:
        logging.error(e)
        messageStack = "";
        for message in MessageQueue:
            if(LLM == "Gemini"):
                messageStack += "{ role: " + message["role"] + ", parts[0]: \"" + message["parts"][0] + "\" }\n"
            else:
                messageStack += "{ role: " + message["role"] + ", content: \"" + message["content"] + "\" }\n"
        return func.HttpResponse(f"Error! {str(e)}\nSession ID: {str(SessionID)}\nPrompt: \"{MyPrompt}\"\nMessages sent: \n{messageStack}", status_code=200)

#Get a response from OpenAI
def CallAI(prompt,SessionID,UseQuestions):
    global MessageQueue
    MessageQueue = []
    SavePrompt(prompt,SessionID)
    
    #Get the Full Conversation
    Conversation = getConversation(SessionID)

    #Get the study results record:
    StudyRecord = getStudyRecord(SessionID)
    
    #Depending on how far along we are in the process determines how we format the conversation
    #Vary the system message depending on if we are doing question-asking or not:
    if(UseQuestions):
        addMessage("system", "You are a helpful assistant designed to help users create short, high-quality documents by asking insightful questions to clarify the users needs and make them think about things they have not considered, and then create high-quality professional documents after discussing the details with the user.")
    else:
        addMessage("system", "You are a helpful assistant designed to help users create short, high-quality professional documents.")

    #if there is no record, or the questions have not been filled out yet, then we can simply include the full conversation log:
    if (StudyRecord == None or StudyRecord.Q1 == None or StudyRecord.Q1 == ""):
        #Add in each line of the conversation that has occurred so far:
        for row in Conversation:
            if(row.prompt != None): addMessage("user", row.prompt)
            if(row.response != None): addMessage("assistant", row.response)
    
    else:
        #if the questions have been filled out, then we need to format the conversation to include the questions and answers. 
        #We are manually overwriting the way the conversation has actually played out with an idealized version. 
        #However, we only do this if the "UseQuestions" parameter is set to "yes":
        addMessage("user", StudyRecord.Prompt)
        if (UseQuestions):
            addMessage("assistant", StudyRecord.Q1)
            addMessage("user", StudyRecord.A1)
            addMessage("assistant", StudyRecord.Q2)
            addMessage("user", StudyRecord.A2)
            addMessage("assistant", StudyRecord.Q3)
            addMessage("user", StudyRecord.A3)
       
        #If there are no documents created yet, add a final prompt instructing the LLM to create the document based on these questions and answers. 
        #This will be the expected prompt at this point. This is only neccessary in the question-inclusive scenario.
        if(StudyRecord.DocQA == None or StudyRecord.DocQA == ""): 
            if(UseQuestions):
                addMessage("assistant", "Thank you for your answers. I will now create a document based on the questions and answers you have provided. Do you have any further instructions?")
                addMessage("user", prompt)

        #After the documents are created, we are doing revisions. So, we will want to include the idealized conversation up to this point, 
        #and then the actual rows of conversation after the documents were created.
        #We need to determine which document to use:
        else:
            if(UseQuestions):
                addMessage("assistant", StudyRecord.DocQA)
                if(StudyRecord.RevisionPromptQA1 != None and StudyRecord.RevisionPromptQA1 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptQA1)
                    addMessage("assistant", StudyRecord.RevisedDocQA1)
                if(StudyRecord.RevisionPromptQA2 != None and StudyRecord.RevisionPromptQA2 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptQA2)
                    addMessage("assistant", StudyRecord.RevisedDocQA2)
                if(StudyRecord.RevisionPromptQA3 != None and StudyRecord.RevisionPromptQA3 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptQA3)
                    addMessage("assistant", StudyRecord.RevisedDocQA3)
            else:
                addMessage("assistant", StudyRecord.DocBaseline)
                if(StudyRecord.RevisionPromptBaseline1 != None and StudyRecord.RevisionPromptBaseline1 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptBaseline1)
                    addMessage("assistant", StudyRecord.RevisedDocBaseline1)
                if(StudyRecord.RevisionPromptBaseline2 != None and StudyRecord.RevisionPromptBaseline2 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptBaseline2)
                    addMessage("assistant", StudyRecord.RevisedDocBaseline2)
                if(StudyRecord.RevisionPromptBaseline3 != None and StudyRecord.RevisionPromptBaseline3 != ""):  
                    addMessage("user", StudyRecord.RevisionPromptBaseline3)
                    addMessage("assistant", StudyRecord.RevisedDocBaseline3)
            #Added in this system message, since GPT3.5 was not re-writing the document, but only addressing the latest thing the user asked for.
            addMessage("user", f"The user has provided some additional feedback. Please re-write the entire document, modifying the original based on this new feedback: \"{prompt}\"")


    global LLM
    #Determine the model to use:
    myModel = ""
    if LLM == "GPT3.5": myModel = "gpt-3.5-turbo"
    elif LLM == "GPT4": myModel = "gpt-4-turbo-preview"
    elif LLM == "Gemini": myModel = "gemini-pro"
    else: myModel = "gpt-3.5-turbo"

    #get a response from the AI:
    response = ""
    responseMessage = ""

    #Call OpenAI
    if(LLM == "GPT3.5" or LLM == "GPT4"):
        SecretKey = os.getenv('OpenAIKey')
        openai.api_key = SecretKey
        client = openai.OpenAI(api_key = SecretKey)
        try:
            response = client.chat.completions.create(
                model = myModel
                , messages = MessageQueue
            )
            #Extract the response:
            responseMessage = response.choices[0].message.content
        except Exception as e:
            logging.error(e)
            responseMessage = "Error getting a response from OpenAI! " + str(e)

    elif(LLM == "Gemini"):
        gemini.configure(api_key = os.getenv('GeminiKey'))
        #Gemini is not as reliable as OpenAI, and sometimes simply fails to return a result. So, we will try up to 3 times:
        tries = 3
        error = True
        while (tries > 0 and error):
            try:
                client = gemini.GenerativeModel('models/gemini-pro')
                response = client.generate_content(MessageQueue)
                responseMessage = response.text
                error = False
            except Exception as e:
                logging.error(e)
                responseMessage = "Error getting a response from Gemini! " + str(e)
                tries -= 1

    #Save the response to the db
    SaveResponse(responseMessage,SessionID)
    #Return the response
    return responseMessage

    
###################################################################################
## Save the prompt and response to the database
###################################################################################
def SavePrompt(prompt,SessionID):
    try:
        prompt = prompt.replace("'","''") 
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"EXEC SavePrompt @SessionID = {SessionID}, @Prompt = '{prompt}'"
        # Table should be created ahead of time in production app.
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            return f"Error writing to DB! SQL attempted: {sql}"
        else: return e.message
    return "DB Write Success!"

def SaveResponse(response,SessionID):
    try:
        response = response.replace("'","''") 
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"EXEC SaveResponse @SessionID = {SessionID}, @Response = '{response}'"
        # Table should be created ahead of time in production app.
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            return "Error writing to DB! SQL attempted: " + sql 
        else: return "Error writing to DB! SQL variable never initialized."
    return "DB Write Success!"
    
###################################################################################
## Connect to the tixclarifyingquestions database and return the connection object
###################################################################################
def get_conn():

    #print(pyodbc.drivers())
    server = 'tixclarifyingquestions.database.windows.net'
    database = 'ClarifyingQuestionsData'
    username = 'ClarifyingQuestions'
    password = os.getenv('SQLPassword') 
    driver= '{ODBC Driver 18 for SQL Server}'
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn


    
###################################################################################
## Get the conversation log up to this point:
###################################################################################
def getConversation(SessionID):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"SELECT * FROM PromptLog WHERE SessionID = {SessionID} ORDER BY promptNum"
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error getting conversation log! Error: " + str(e)
        else: return "Error writing to DB! SQL variable never initialized."

        
###################################################################################
## Get the recorded study responses up to this point:
###################################################################################
def getStudyRecord(SessionID):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"SELECT * FROM StudyResults WHERE SessionID = " + SessionID
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result[0]
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error getting study results! Error: " + str(e)
        else: return "Error writing to DB! SQL variable never initialized."

        
###################################################################################
## A function to add a new message to the queue. 
## Formats the message differently according to the LLM being used.
###################################################################################
def addMessage(Role, Message):
    global MessageQueue
    global LLM
    #input washing:
    if(Message == None): return MessageQueue
    if LLM == "GPT3.5" or LLM == "GPT4":
        MessageQueue.append({"role": Role, "content": Message})
    elif LLM == "Gemini":
        newRole = ""
        if(Role == "assistant"): newRole = "model"
        if(Role == "system"): newRole = "user" #return MessageQueue #Gemini does not suport systems messages. May need to find a better way to do this. # 
        if(Role == "user"): newRole = "user"
        MessageQueue.append({"role": newRole, "parts": [Message]})
        if(Role == "system"): MessageQueue.append({"role": "model", "parts": ["OK!"]})
    else:
        MessageQueue.append({"role": Role, "content": Message})

    #return MessageQueue