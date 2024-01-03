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
        else: return "Error writing to DB! SQL variable never initialized."
    return "DB Write Success for session ID " + SessionID

###################################################################################
## Connect to the tixclarifyingquestions database and return the connection object
###################################################################################
def get_conn():
    connection_string = os.getenv('SQLConnectionString')
    conn = pyodbc.connect(connection_string)
    return conn