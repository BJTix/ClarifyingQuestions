import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = req.params.get('SessionID')
    Age = req.params.get('Age')
    Gender = req.params.get('Gender')
    Experience = req.params.get('Experience')
    English = req.params.get('English')

    if not SessionID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            SessionID = req_body.get('SessionID')
            Age = req_body.get('Age')
            Gender = req_body.get('Gender')
            Experience = req_body.get('Experience')
            English = req_body.get('English')

    #input washing:
    if(SessionID == None or not SessionID.isnumeric()):
        return "SessionID must be a number! Received: " + SessionID
    if(Age == None or not Age.isnumeric()):
        return "Age must be a number! Received: " + Age
    if(Experience == None or not Experience.isnumeric()):
        return "Experience must be a number! Received: " + Experience
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE PilotStudyResults SET Age = "+ Age +", Gender = '" + Gender + "', ExperienceLevel = " + Experience + ", EnglishPrimary = '" + English + "' WHERE SessionID = " + SessionID
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