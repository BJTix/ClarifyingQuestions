/*
Created: 2023-11-30
Author: Bernadette J Tix
Description:
    Reserves a new session ID and returns the new session ID. 
    This creates a new line in PromptLog that contains only the sessionID
*/
ALTER PROCEDURE ReserveSessionID AS BEGIN

    DECLARE @newID INT
    SELECT @newID = ISNULL(MAX(ISNULL(sessionid,0)),0) + 1 FROM PromptLog
    INSERT INTO PromptLog(sessionID, promptNum) VALUES (@newID, 0)
    SELECT newID = @newID

END