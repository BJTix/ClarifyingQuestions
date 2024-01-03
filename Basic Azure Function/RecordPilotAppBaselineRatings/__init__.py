import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = req.params.get('SessionID')    
    #Prompt and discussion
    BaselineCloseness = req.params.get('BaselineCloseness')
    BaselineUsefulness = req.params.get('BaselineUsefulness')
    BaselineOverall = req.params.get('BaselineOverall')

    if not SessionID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SessionID = req_body.get('SessionID')
            #Prompt and discussion
            BaselineCloseness = req_body.get('BaselineCloseness')
            BaselineUsefulness = req_body.get('BaselineUsefulness')
            BaselineOverall = req_body.get('BaselineOverall')

    #input washing:
    if(SessionID == None or not SessionID.isnumeric()):
        return "SessionID must be a number! Received: " + SessionID
    if(BaselineCloseness == None or not BaselineCloseness.isnumeric()):
        return "BaselineCloseness must be a number! Received: " + BaselineCloseness
    if(BaselineUsefulness == None or not BaselineUsefulness.isnumeric()):
        return "BaselineUsefulness must be a number! Received: " + BaselineUsefulness
    if(BaselineOverall == None or not BaselineOverall.isnumeric()):
        return "BaselineOverall must be a number! Received: " + BaselineOverall

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE PilotStudyResults SET BaselineCloseness = " + BaselineCloseness + ", BaselineUsefulness = " + BaselineUsefulness \
            + ", BaselineOverall = " + BaselineOverall + " WHERE SessionID = " + SessionID
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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn