import logging
import openai
import azure.functions as func
import pyodbc

SecretKey = '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'
openai.api_key = SecretKey

def main(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    MyPrompt = ""
    SessionID = 0
    try:
        req_body = req.get_json()
        MyPrompt = req_body.get('prompt')
    except:
        return "No prompt provided!"
    
    Output = CallOpenAI(MyPrompt)

    #Save the message in a database:

    #Return as json:
    
    #toDoItems.set(func.SqlRow({"id": uuid.uuid4(), "messageTime": datetime.now, "introMessage": Output}))
    return func.HttpResponse(Output, status_code=200)
    #return func.HttpResponse({"answer":Output}, status_code=200)

#Get a response from OpenAI
def CallOpenAI(prompt):
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
    return response.choices[0].message.content
    #return response.['choices'][0]['message']['content']
    #return openai.VERSION

def SavePrompt(prompt):
    try:
        messageToSave = messageToSave.replace("'","''") 
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"INSERT INTO dbo.TestIntroMessage(pk, promptTime, prompt) VALUES(ISNULL((SELECT MAX(pk) FROM TestIntroMessage),0) + 1," \
        + "SYSDATETIME() AT TIME ZONE 'Alaskan Standard Time','" + prompt + "')"
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
    password = 'hEkjqGakb4mY2f3'   
    driver= '{ODBC Driver 18 for SQL Server}'
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
    conn = pyodbc.connect(connection_string)
    return conn