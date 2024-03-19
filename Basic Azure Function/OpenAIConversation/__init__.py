import logging
import openai
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    MyPrompt = ""
    SessionID = 0
    try:
        req_body = req.get_json()
        MyPrompt = req_body.get('prompt')
        SessionID = req_body.get('sessionid')
        LLM = req_body.get('LLM')
        UseQuestions = (req_body.get('UseQuestions') == "yes")
    except:
        return "Parameter Error!    Usage: {\"prompt\":\"<Prompt Text>\",\"sessionid\":<SessionID>,\"LLM\":\"GPT3\", \"UseQuestions\":\"yes\"}"

    Output = CallOpenAI(MyPrompt,SessionID,LLM,UseQuestions)
    return func.HttpResponse(Output, status_code=200)

#Get a response from OpenAI
def CallOpenAI(prompt,SessionID,LLM,UseQuestions):
    SecretKey = os.getenv('OpenAIKey')
    openai.api_key = SecretKey
    SavePrompt(prompt,SessionID)
    
    #Get the Full Conversation
    Conversation = getConversation(SessionID)

    #Get the study results record:
    StudyRecord = getStudyRecord(SessionID)
    
    #Depending on how far along we are in the process determines how we format the conversation
    myMessages = []
    myMessages.append({"role": "system", "content": "You are a helpful assistant designed to help users create short documents by asking insightful questions to clarify the users needs and make them think about things they have not considered, and then create high-quality professional documents after discussing the details with the user."})

    #if there is no record, or the questions have not been filled out yet, then we can simply include the full conversation log:
    if (StudyRecord is None or len(StudyRecord) == 0 or StudyRecord.Q1 is None):
        #format the conversation for ChatGPT parameters
        for row in Conversation:
            myMessages.append({"role" : "user", "content" : row.prompt})
            if(row.response is not None): myMessages.append({"role" : "assistant", "content" : row.response})
    
    else:
        #if the questions have been filled out, then we need to format the conversation to include the questions and answers. 
        #We are manually overwriting the way the conversation has actually played out with an idealized version. 
        #However, we only do this if the "UseQuestions" parameter is set to "yes":
        myMessages.append({"role" : "user", "content" : row.prompt})
        if (UseQuestions):
            myMessages.append({"role" : "assistant", "content" : StudyRecord.Q1})
            myMessages.append({"role" : "user", "content" : StudyRecord.A1})
            myMessages.append({"role" : "assistant", "content" : StudyRecord.Q2})
            myMessages.append({"role" : "user", "content" : StudyRecord.A2})
            myMessages.append({"role" : "assistant", "content" : StudyRecord.Q3})
            myMessages.append({"role" : "user", "content" : StudyRecord.A3})
            #If there are no documents created yet, add a final prompt instructing the LLM to create the document based on these questions and answers. 
            #This will be the expected prompt at this point. This is only neccessary in the question-inclusive scenario.
            if(StudyRecord.DocQA is None): myMessages.append({"role" : "system", "content" : prompt})

        #After the documents are created, we are doing revisions. So, we will want to include the idealized conversation up to this point, 
        #and then the actual rows of conversation after the documents were created.
        #We need to determine which document to use:
        if(UseQuestions & StudyRecord.DocQA is not None):
            myMessages.append({"role" : "assistant", "content" : StudyRecord.DocQA})
            if(StudyRecord.RevisionPromptQA1 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptQA1})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocQA1})
            if(StudyRecord.RevisionPromptQA2 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptQA2})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocQA2})
            if(StudyRecord.RevisionPromptQA3 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptQA3})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocQA3})
            myMessages.append({"role" : "user", "content" : prompt})
        else:
            myMessages.append({"role" : "assistant", "content" : StudyRecord.DocBaseline})
            if(StudyRecord.RevisionPromptBaseline1 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptBaseline1})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocBaseline1})
            if(StudyRecord.RevisionPromptBaseline2 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptBaseline2})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocBaseline2})
            if(StudyRecord.RevisionPromptBaseline3 is not None):  
                myMessages.append({"role" : "user", "content" : StudyRecord.RevisionPromptBaseline3})
                myMessages.append({"role" : "system", "content" : StudyRecord.RevisedDocBaseline3})
            myMessages.append({"role" : "user", "content" : prompt})


    #Determine the model to use:
    myModel = ""
    if LLM == "GPT3": myModel = "gpt-3.5-turbo"
    elif LLM == "GPT4": myModel = "gpt-4-turbo-preview"
    else: myModel = "gpt-3.5-turbo"

    #Call OpenAI
    client = openai.OpenAI(api_key =  SecretKey)
    response = client.chat.completions.create(
        model = myModel
        , messages = myMessages
    )

    #Extract the response:
    responseMessage = response.choices[0].message.content
    #Save the response to the db
    SaveResponse(responseMessage,SessionID)
    #Return the response
    return responseMessage

def SavePrompt(prompt,SessionID):
    try:
        prompt = prompt.replace("'","''") 
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"EXEC SavePrompt @SessionID = " + SessionID + ", @Prompt = '" + prompt + "'"
        # Table should be created ahead of time in production app.
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            return "Error writing to DB! SQL attempted: " + sql
        else: return e.message
    return "DB Write Success!"

def SaveResponse(response,SessionID):
    try:
        response = response.replace("'","''") 
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"EXEC SaveResponse @SessionID = " + SessionID + ", @Response = '" + response + "'"
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
        sql = f"SELECT * FROM PromptLog WHERE SessionID = " + SessionID + " ORDER BY promptNum"
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
        return result
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error getting study results! Error: " + str(e)
        else: return "Error writing to DB! SQL variable never initialized."