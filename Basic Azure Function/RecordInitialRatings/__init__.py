import logging
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        SessionID = req_body.get('SessionID')
        #Prompt and discussion
        Preference = req_body.get('Preference')
        Usefulness = req_body.get('Usefulness')
        BaselineFeedback = req_body.get('BaselineFeedback')
        QAFeedback = req_body.get('QAFeedback')
    except ValueError:
        return "Parameter Error!"

    #input washing:    
    BaselineFeedback = BaselineFeedback.replace("'", "''")
    QAFeedback = QAFeedback.replace("'", "''")

    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE StudyResults SET OverallPreference = " + Preference + ", UsefulnessPreference = " + Usefulness \
            + ", DocBaselineFeedback = '" + BaselineFeedback + "', DocQAFeedback = '" + QAFeedback + "' WHERE SessionID = " + SessionID
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