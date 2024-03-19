import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        SessionID = req_body.get('SessionID')
        LLM = req_body.get('LLM')
        #Prompt and discussion
        Prompt = req_body.get('Prompt')
        Q1 = req_body.get('Q1')
        A1 = req_body.get('A1')
        Q2 = req_body.get('Q2')
        A2 = req_body.get('A2')
        Q3 = req_body.get('Q3')
        A3 = req_body.get('A3')
    except ValueError:
        return "Parameter Error!"
    
    #input washing:
    Prompt = Prompt.replace("'", "''")
    Q1 = Q1 .replace("'", "''")
    A1 = A1.replace("'", "''")
    Q2 = Q2.replace("'", "''")
    A2 = A2.replace("'", "''")
    Q3 = Q3.replace("'", "''")
    A3 = A3.replace("'", "''")

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE StudyResults SET Prompt = '"+ Prompt +"', Q1 = '" + Q1 + "', A1 = '" + A1 + "', Q2 = '" + Q2 + "', A2 = '" + A2 + "', Q3 = '" + Q3 + "', A3 = '" + A3\
        + "', LLM = '" + LLM + "' WHERE SessionID = " + SessionID
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error writing to DB! SQL attempted: " + sql
        else: return "Error writing to DB! " +  e.message
    return "DB Write Success for session ID " + SessionID

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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password +';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn