import logging
import openai
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    SessionID = 0
    try:
        req_body = req.get_json()
        SessionID = req_body.get('SessionID')
        Instructions = req_body.get('Instructions')
        newDoc = req_body.get('newDoc')
        UseQuestions = (req_body.get('UseQuestions') == "yes")
    except:
        return "Parameter Error!"

    #Get the existing record
    StudyRecord = getStudyRecord(SessionID)

    #input wash the text:
    Instructions = Instructions.replace("'","''")
    newDoc = newDoc.replace("'","''")

    #Determine how many refinements have been done:
    Step = 1
    if(UseQuestions):
        if(StudyRecord.RevisionPromptQA1 != None and StudyRecord.RevisionPromptQA1 != ""): Step = 2
        if(StudyRecord.RevisionPromptQA2 != None and StudyRecord.RevisionPromptQA2 != ""): Step = 3
        sql = f"UPDATE StudyResults SET RevisionPromptQA{Step} = '{Instructions}', RevisedDocQA{Step} = '{newDoc}' WHERE SessionID = {SessionID}"
    else:
        if(StudyRecord.RevisionPromptBaseline1 != None and StudyRecord.RevisionPromptBaseline1 != ""): Step = 2
        if(StudyRecord.RevisionPromptBaseline2 != None and StudyRecord.RevisionPromptBaseline2 != ""): Step = 3
        sql = f"UPDATE StudyResults SET RevisionPromptBaseline{Step} = '{Instructions}', RevisedDocBaseline{Step} = '{newDoc}' WHERE SessionID = {SessionID}"

    #record the new result:
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            return "Error writing to DB! SQL attempted: " + sql
        else: return e.message

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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn

        
###################################################################################
## Get the recorded study responses up to this point:
###################################################################################
def getStudyRecord(SessionID):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = f"SELECT * FROM StudyResults WHERE SessionID = " + SessionID
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result[0]
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error getting study results! Error: " + str(e)
        else: return "Error writing to DB! SQL variable never initialized."
