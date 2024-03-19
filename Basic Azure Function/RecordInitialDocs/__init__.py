import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        SessionID = req_body.get('SessionID')
        #Documents
        DocBaseline = req_body.get('DocBaseline')
        DocQA = req_body.get('DocQA')
        ShowQAFirst = req_body.get('ShowQAFirst')
    except ValueError:
        return "Parameter Error!"
    
    #input washing:
    DocBaseline = DocBaseline.replace("'", "''")
    DocQA = DocQA.replace("'", "''")

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE StudyResults SET DocBaseline = '" + DocBaseline + "', DocQA = '" + DocQA + "', ShowQAFirst = " + ShowQAFirst + " WHERE SessionID = " + SessionID
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