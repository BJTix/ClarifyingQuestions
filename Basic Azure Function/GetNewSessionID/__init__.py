import logging
import pyodbc
import azure.functions as func
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
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
    return  func.HttpResponse(str(newID), status_code=200)
    
    
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
    connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
    conn = pyodbc.connect(connection_string)
    return conn