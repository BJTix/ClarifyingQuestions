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
    except:
        return "No prompt provided!"

    Output = CallOpenAI(MyPrompt,SessionID,LLM)
    return func.HttpResponse(Output, status_code=200)

#Get a response from OpenAI
def CallOpenAI(prompt,SessionID,LLM):
    SecretKey = os.getenv('OpenAIKey')
    openai.api_key = SecretKey
    SavePrompt(prompt,SessionID)
    
    #Get the Full Conversation
    Conversation = getConversation(SessionID)

    #format the conversation for ChatGPT parameters
    myMessages = []
    myMessages.append({"role": "system", "content": "You are a helpful assistant designed to help users create short documents by asking insightful questions to clarify the users needs and make them think about things they have not considered, and then create high-quality professional documents after discussing the details with the user."})
    for row in Conversation:
        myMessages.append({"role" : "user", "content" : row.prompt})
        if(row.response is not None): myMessages.append({"role" : "assistant", "content" : row.response})

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