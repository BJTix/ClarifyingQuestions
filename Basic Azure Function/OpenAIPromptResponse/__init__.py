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
    except:
        return "No prompt provided!"
    
    Output = CallOpenAI(MyPrompt,SessionID)
    return func.HttpResponse(Output, status_code=200)

#Get a response from OpenAI
def CallOpenAI(prompt,SessionID):
    SecretKey = os.getenv('OpenAIKey')
    openai.api_key = SecretKey
    SavePrompt(prompt,SessionID)
    client = openai.OpenAI(api_key =  SecretKey)
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo"
        #, prompt = MyPrompt 
        #, max_tokens = 200 #~4 tokens per word
        #, temperature = 0 #lower temperature = less random. Scale 0~1 ish
        , messages = [
            {"role": "system", "content": "You are a helpful assistant."}
            , {"role" : "user", "content" : prompt}
        ]
    )
    responseMessage = response.choices[0].message.content
    SaveResponse(responseMessage,SessionID)
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
            #print(sql)
            return "Error writing to DB! SQL attempted: " + sql
        else: return "Error writing to DB! SQL variable never initialized."
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
            #print(sql)
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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn