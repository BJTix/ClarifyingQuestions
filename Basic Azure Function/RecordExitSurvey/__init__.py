import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"UPDATE StudyResults SET ExitAnnoying = {ExitAnnoying}, ExitEngaged = {ExitEngaged}, ExitWilling = {ExitWilling}\
, ExitTwoOptions = {ExitTwoOptions}, ExitFeedback = '{ExitFeedback}', CompletedAt = GETDATE() WHERE SessionID = {SessionID}"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return f"Error writing to DB! SQL attempted: {sql}"
        else: return "Error writing to DB! " +  e.message

    #Check if we need to backtrack and update the previous session's record:
    #Get the old record: 
    oldRecord = getStudyRecord(SessionID)
    if oldRecord == None:
        return "No record found for session ID " + SessionID

    while(oldRecord.PreviousSession != None):
        try:
            conn = get_conn()
            cursor = conn.cursor()
            sql = f"UPDATE StudyResults SET ExitAnnoying = {ExitAnnoying}, ExitEngaged = {ExitEngaged}, ExitWilling = {ExitWilling}\
, ExitTwoOptions = {ExitTwoOptions}, ExitFeedback = '{ExitFeedback}', CompletedAt = GETDATE() WHERE SessionID = {oldRecord.PreviousSession}"
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error(e)
            if 'sql' in locals(): 
                #print(sql)
                return f"Error writing to DB! SQL attempted: {sql}"
            else: return "Error writing to DB! " +  e.message
        if(oldRecord.PreviousSession != None):
            oldRecord = getStudyRecord(oldRecord.PreviousSession)

    return f"DB Write Success for session ID {SessionID}"

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

###################################################################################
## Get the recorded study responses up to this point:
###################################################################################
def getStudyRecord(SessionID):
    logging.info('Reserving StudyResults log for SessionID: ' + str(SessionID))
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"SELECT * FROM StudyResults WHERE SessionID = " + str(SessionID)
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result[0]
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            logging.info('Error in sql: ' + sql)
            logging.info("Error getting study results! Error: " + str(e))
            return None
        else: None
