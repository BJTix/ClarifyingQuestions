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
    connection_string = os.getenv('SQLConnectionString')
    conn = pyodbc.connect(connection_string)
    return conn