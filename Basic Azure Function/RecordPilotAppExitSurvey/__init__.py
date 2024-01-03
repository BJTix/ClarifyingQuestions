import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = req.params.get('SessionID')    
    #Prompt and discussion
    ExitAnnoying = req.params.get('ExitAnnoying')
    ExitEngaged = req.params.get('ExitEngaged')
    ExitWilling = req.params.get('ExitWilling')
    ExitTwoOptions = req.params.get('ExitTwoOptions')
    ExitFeedback = req.params.get('ExitFeedback')

    if not SessionID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SessionID = req_body.get('SessionID')
            #Prompt and discussion
            ExitAnnoying = req_body.get('ExitAnnoying')
            ExitEngaged = req_body.get('ExitEngaged')
            ExitWilling = req_body.get('ExitWilling')
            ExitTwoOptions = req_body.get('ExitTwoOptions')
            ExitFeedback = req_body.get('ExitFeedback')

    #input washing:
    ExitFeedback = ExitFeedback.replace("'", "''")

    #input washing:
    if(SessionID == None or not SessionID.isnumeric()):
        return "SessionID must be a number! Received: " + SessionID
    if(ExitAnnoying == None or not ExitAnnoying.isnumeric()):
        return "ExitAnnoying must be a number! Received: " + ExitAnnoying
    if(ExitEngaged == None or not ExitEngaged.isnumeric()):
        return "ExitEngaged must be a number! Received: " + ExitEngaged
    if(ExitWilling == None or not ExitWilling.isnumeric()):
        return "ExitWilling must be a number! Received: " + ExitWilling
    if(ExitTwoOptions == None or not ExitTwoOptions.isnumeric()):
        return "ExitTwoOptions must be a number! Received: " + ExitTwoOptions

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE PilotStudyResults SET ExitAnnoying = " + ExitAnnoying + ", ExitEngaged = " + ExitEngaged + ", ExitWilling = " + ExitWilling +\
              ", ExitTwoOptions = " + ExitTwoOptions + ", ExitFeedback = '" + ExitFeedback + "', CompletedAt = GETDATE() WHERE SessionID = " + SessionID
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