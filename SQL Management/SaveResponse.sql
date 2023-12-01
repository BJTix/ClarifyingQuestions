/*
Created: 2023-11-30
Author: Bernadette J Tix
Description:
    Saves a response for the given session.
    Automatically generates prompt number and time.
*/
ALTER PROCEDURE SaveResponse @SessionID INT, @Response VARCHAR(MAX) AS BEGIN
    
    DECLARE @errormsg VARCHAR(100)
    --Input washing for session ID:
    IF NOT EXISTS (SELECT * FROM PromptLog WHERE sessionID = @SessionID) BEGIN
        SET @errormsg = CONCAT('The session ID ', @SessionID, ' has not been reserved!');
        THROW 51000, @errormsg, 1;
    END

    --Get the latest row number:
    DECLARE @promptNum INT
    SELECT @promptNum = MAX(ISNULL(promptNum,0)) FROM PromptLog WHERE sessionID = @SessionID

    --Sequence washing, make sure this is called in the right order:
    IF (0 = @promptNum) OR EXISTS (SELECT * FROM PromptLog WHERE sessionID = @SessionID AND promptNum = @promptNum AND response IS NOT NULL) BEGIN
        SET @errormsg = CONCAT('The session ID ', @SessionID, ' is ready for a new prompt, not a response!');
        THROW 51000, @errormsg, 1;
    END

    --Since row numbers are suppossed to be reserved ahead of time, the first prompt will have a row in the table already.
    UPDATE PromptLog SET response = @Response, responseTime = SYSDATETIME() AT TIME ZONE 'Alaskan Standard Time' WHERE sessionID = @SessionID AND promptNum = @promptNum

END