/*
Created: 2023-11-30
Author: Bernadette J Tix
Description:
    Saves a new prompt for the given session.
    Automatically generates prompt number and time.
*/
ALTER PROCEDURE SavePrompt @SessionID INT, @Prompt VARCHAR(MAX) AS BEGIN
    
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
    IF EXISTS (SELECT * FROM PromptLog WHERE sessionID = @SessionID AND promptNum = @promptNum AND prompt IS NOT NULL) BEGIN
        SET @errormsg = CONCAT('The session ID ', @SessionID, ' is ready for a response, not a new prompt!');
        THROW 51000, @errormsg, 1;
    END

    --Since row numbers are suppossed to be reserved ahead of time, the first prompt will have a row in the table already.
    IF (0 = @promptNum) BEGIN
        UPDATE PromptLog SET promptNum = 1, prompt = @Prompt, promptTime = SYSDATETIME() WHERE sessionID = @SessionID
    END ELSE BEGIN
        INSERT INTO PromptLog (sessionid, promptNum, prompt, promptTime)
        VALUES(@SessionID,@promptNum + 1,@Prompt, SYSDATETIME())
    END

END