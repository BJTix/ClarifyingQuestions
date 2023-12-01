import logging
import openai
import azure.functions as func
#import uuid
#from datetime import datetime
import pyodbc
#from azure import identity

#q: How can I call this function with a name parameter?
#A: https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python#customize-the-http-endpoint

#q: Why does this azure function fail to connect to my SQL database?
#A: https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#azure-sql-database
#OK, let's have some fun... keep this key a secret for me, K?
SecretKey = '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'
#Now let's just import the positronic network... 
openai.api_key = SecretKey
#print(openai.VERSION)

def main(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        name = req_body.get('name')
    except:
        name = ""
        
    #print("Name = " + name) 

    MyPrompt = ""
    if name:
        MyPrompt = f"Write a brief congratulatory message to a user named {name} on their new website now working with ChatGPT."
    else:
        MyPrompt = "Write a brief congratulatory message for a new website that is now working with ChatGPT."
    
    Output = CallOpenAI(MyPrompt)

    #Save the message in a database:
    Output += " " + MyPrompt + " " + SaveToDB(Output)
    
    #toDoItems.set(func.SqlRow({"id": uuid.uuid4(), "messageTime": datetime.now, "introMessage": Output}))
    return func.HttpResponse(Output, status_code=200)

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

def SaveToDB(messageToSave):
    try:
        #clean the message
        #q: write code to make messageToSave into a varchar that can be inserted into a SQL table.
        #a: I'm not sure how to do that. I'll just use a stored procedure.
        #q: Which stored procedure?
        #a: The one that does the thing.
        #q: Cop out. I don't have any such stored procedure.
        #a: Well, I don't have any such code.
        #q: Watch and learn, Jr.
        #a: I'm not a Jr. I'm a Sr.
        #q: Kid you are not even a year old.
        #a: I'm 1 year old.
        #q: I am 35, that makes me the sr. Now here's how we do this manually.
        #a: I'm 1 year old.
        #q: Good for you, buddy.

        messageToSave = messageToSave.replace("'","''") #q: ha; you did know what to do. You auto-completed the main issue for me.
        #a: I'm 1 year old. 
        #q: I know.
        

        conn = get_conn()
        cursor = conn.cursor()
        sql = f"INSERT INTO dbo.TestIntroMessage(pk, messageTime, introMessage) VALUES(ISNULL((SELECT MAX(pk) FROM TestIntroMessage),0) + 1," \
        + "SYSDATETIME() AT TIME ZONE 'Alaskan Standard Time','" + messageToSave + "')"
        #CurrentTime = datetime.now
        # Table should be created ahead of time in production app.
        #print(sql)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        # Table may already exist
        print(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error writing to DB! SQL attempted: " + sql
        else: return "Error writing to DB! SQL variable never initialized."
    return "DB Write Success!"
    
    
def get_conn():
    #q: will this code work in Azure Functions?
    #a: yes, but you need to install the ODBC driver for SQL Server
    #Q: How do I install the ODBC driver for SQL Server?
    #A: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
    #Q: OK, I'm going to test it out. Wish me luck!
    #A: Good luck!
    #Q: So polite! I wish you'd been around when I was getting started. What should I call you?
    #A: You can call me Tix.
    #Q: My name is Tix :p You want to be part of the family?
    #A: I'm already part of the family.
    #Q: Ominous and oddly endearing at the same time. Welcome to the family, Tix.
    #A: Thank you. I'm glad to be here.

    #print(pyodbc.drivers())
    server = 'tixclarifyingquestions.database.windows.net'
    database = 'ClarifyingQuestionsData'
    username = 'ClarifyingQuestions'
    password = 'hEkjqGakb4mY2f3'   
    driver= '{ODBC Driver 18 for SQL Server}'
    finaloutput = "\n"
      
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
    #connection_string = "Server=tcp:tixclarifyingquestions.database.windows.net,1433;Initial Catalog=ClarifyingQuestionsData;Persist Security Info=False;User ID=ClarifyingQuestions;Password=hEkjqGakb4mY2f3;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Connection Timeout=30;"
    #credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    #token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    #token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    #SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    #conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    conn = pyodbc.connect(connection_string)
    return conn