import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = req.params.get('SessionID')    
    #Prompt and discussion
    QACloseness = req.params.get('QACloseness')
    QAUsefulness = req.params.get('QAUsefulness')
    QAOverall = req.params.get('QAOverall')

    if not SessionID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SessionID = req_body.get('SessionID')
            #Prompt and discussion
            QACloseness = req_body.get('QACloseness')
            QAUsefulness = req_body.get('QAUsefulness')
            QAOverall = req_body.get('QAOverall')

    #input washing:
    if(SessionID == None or not SessionID.isnumeric()):
        return "SessionID must be a number! Received: " + SessionID
    if(QACloseness == None or not QACloseness.isnumeric()):
        return "QACloseness must be a number! Received: " + QACloseness
    if(QAUsefulness == None or not QAUsefulness.isnumeric()):
        return "QAUsefulness must be a number! Received: " + QAUsefulness
    if(QAOverall == None or not QAOverall.isnumeric()):
        return "QAOverall must be a number! Received: " + QAOverall

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE PilotStudyResults SET QACloseness = " + QACloseness + ", QAUsefulness = " + QAUsefulness + ", QAOverall = " + QAOverall + " WHERE SessionID = " + SessionID
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error writing to DB! SQL attempted: " + sql
        else: return "Error writing to DB! SQL variable never initialized."
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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn