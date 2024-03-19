
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
--DELETE PilotStudyResults


UPDATE PilotStudyResults SET Age = @, Gender = @, ExperienceLevel = @, EnglishPrimary = @ WHERE SessionID = @


UPDATE PilotStudyResults SET Age = 35, Gender = F, ExperienceLevel = 2, EnglishPrimary = Y WHERE SessionID = 220

--ALTER TABLE PilotStudyResults ADD CompletedAt DATETIME NULL
SELECT * FROM PromptLog where sessionid = 285 order by sessionID, promptNum
select * from PilotStudyResults where SessionID = 285


select UsefullnessDiff = AVG(QAUsefulness - BaselineUsefulness),
    UsefullnessSTDQA = STDEV(QAUsefulness),
    UsefullnessSTDBL = STDEV(QAUsefulness),
    ClosenessDiff = AVG(QACloseness - BaselineCloseness),
    ClosenessSTDQA = STDEV(QACloseness),
    ClosenessSTDBL = STDEV(BaselineCloseness),
    OverallDiff = AVG(QAOverall - BaselineOverall),
    OverallSTDQA = STDEV(QAOverall),
    OverallSTDBL = STDEV(BaselineOverall)
from PilotStudyResults


SELECT * FROM PromptLog WHERE SessionID = 283 ORDER BY promptNum



UPDATE StudyResults SET Prompt = 'Write an essay on the topic of chivalry in 14th century western Europe.', Q1 = '1. **Aspect Focus**: Could you specify which aspects of chivalry interest you most for this essay? For example, are you looking to explore the martial virtues of knights, the influence of courtly love on literature and society, the intertwining of chivalry with Christian values, or another facet of chivalric culture in 14th-century Western Europe?', A1 = 'The martial virtues of knights and how it impacts our view of morality and virtue today.', Q2 = '2. **Regional Emphasis**: From the broad landscape of Western Europe, are there specific regions or kingdoms (such as the Kingdom of France, the British Isles, the Holy Roman Empire, etc.) whose chivalric traditions and practices you would prefer to focus on? Or would you prefer a comparative approach that highlights differences between regions?', A2 = 'The country of greatest interest is England, but compare and contrast English ideals of chivalry with those found in Italy and France.', Q3 = '3. **Historical Context and Impact**: How important do you find the inclusion of major 14th-century events (like the Black Death, the Hundred Years'' War, the Papal Schism) in shaping and influencing chivalric ideals and practices? Additionally, would you like the essay to touch upon the legacy of these chivalric ideals, possibly tracing their influence to modern concepts of honor and conduct?', A3 = 'Yes! This is very important to the essay!', LLM = 'GPT4' WHERE SessionID = 350