import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = req.params.get('SessionID')
    if not SessionID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SessionID = req_body.get('SessionID')

    #Get the old record:
    oldRecord = getStudyRecord(SessionID)
    if oldRecord == None:
        return "No record found for session ID " + SessionID
    
    #get a new session ID
    newSessionID = getNewSessionID()

    #Create a new record:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"INSERT INTO StudyResults (SessionID, ConsentSigned, PreviousSession, Age, Gender, ExperienceLevel, EnglishPrimary) VALUES (\
{newSessionID},'"+str(oldRecord.ConsentSigned)[0:19]+f"',{SessionID},{oldRecord.Age},'{oldRecord.Gender}',\
{oldRecord.ExperienceLevel},'{oldRecord.EnglishPrimary}')"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return f"Error writing to DB! SQL attempted: " + sql
        else: return e.message
    
    #return the new session ID
    return  func.HttpResponse(str(newSessionID), status_code=200)

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
    logging.info(f"Reserving StudyResults log for SessionID: {SessionID}")
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"SELECT * FROM StudyResults WHERE SessionID = {SessionID}"
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result[0]
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            logging.info(f"Error in sql: {sql}")
            logging.info(f"Error getting study results! Error: " + str(e))
            return None
        else: return None


###################################################################################
## Get the new session ID:
###################################################################################
def getNewSessionID():
    logging.info('Reserving a new session ID.')
    newID = 0
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"EXEC dbo.ReserveSessionID"
        # Table should be created ahead of time in production app.
        cursor.execute(sql)
        sql = f"SELECT newID = MAX(sessionID) FROM PromptLog"
        # Table should be created ahead of time in production app.
        cursor.execute(sql)
        newID = cursor.fetchone()[0]
        conn.commit()
        logging.info('New ID: ' + str(newID))
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error getting a new session ID! Error: " + str(e)
        else: return "Error writing to DB! SQL variable never initialized."
    return newID