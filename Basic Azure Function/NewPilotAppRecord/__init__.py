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
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "INSERT INTO PilotStudyResults (SessionID, ConsentSigned) VALUES ("+SessionID+", GETDATE())"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.error(e)
        if 'sql' in locals(): 
            #print(sql)
            return "Error writing to DB! SQL attempted: " + sql
        else: return "Error writing to DB! SQL variable never initialized."
    return "DB Write Success! Session ID " + SessionID + " has been recorded as having signed the consent form."

###################################################################################
## Connect to the tixclarifyingquestions database and return the connection object
###################################################################################
def get_conn():
    connection_string = os.getenv('SQLConnectionString')
    conn = pyodbc.connect(connection_string)
    return conn