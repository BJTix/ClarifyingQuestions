
--INSERT INTO dbo.TestIntroMessage(pk, messageTime, introMessage) VALUES(ISNULL((SELECT MAX(pk) FROM TestIntroMessage),0) + 1,SYSDATETIME(),'Test')
select [pk],
--UTCTime = [messageTime],
AlaskaTime = dateadd([HOUR],-8,messageTime),
[introMessage] from TestIntroMessage
--truncate table TestIntroMessage



EXEC ReserveSessionID
EXEC SavePrompt @SessionID = 1, @Prompt = 'Test Prompt'
EXEC SaveResponse @SessionID = 4, @Response = 'Test Response'

SELECT * FROM PromptLog order by sessionID, promptNum
SELECT newID = MAX(sessionID) FROM PromptLog

delete PromptLog where promptNum = 0 

INSERT INTO PilotStudyResults (SessionID, ConsentSigned) VALUES (123, GETDATE())

SELECT * FROM PilotStudyResults
DELETE PilotStudyResults


UPDATE PilotStudyResults SET Age = @, Gender = @, ExperienceLevel = @, EnglishPrimary = @ WHERE SessionID = @


UPDATE PilotStudyResults SET Age = 35, Gender = F, ExperienceLevel = 2, EnglishPrimary = Y WHERE SessionID = 220

--ALTER TABLE PilotStudyResults ADD CompletedAt DATETIME NULL