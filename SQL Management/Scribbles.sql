
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



UPDATE StudyResults SET Prompt = 'Write an essay on the topic of chivalry in 14th century western Europe.', Q1 = '1. Can you specify which aspect of chivalry interests you most for this essay—such as the practices of knighthood, the principles of courtly love, or the ethical and moral code of chivalry—and whether you''d like to explore the ideal versus the reality of these practices in 14th century Western Europe?
', A1 = 'Write about how the ideal differed from the practice and how the ideal still impacts culture today.', Q2 = '2. Would you prefer that the essay concentrates on chivalry within a particular country or region in Western Europe, like France or England, to provide a deeper, more nuanced analysis, or should it encompass a broader comparison across different Western European cultures?
', A2 = 'The country of greatest interest is England, but compare and contrast English ideals of chivalry with those found in Italy and France.', Q3 = '3. How do you envision the purpose of this essay? Are you aiming for it to be an academic piece with a focus on historical analysis and interpretation based on primary sources, or are you looking for a more general audience engaging narrative that also includes how perceptions of 14th-century chivalry have been reconstructed or romanticized over time?', A3 = 'This is an essay for a course on historical western martial arts. The course is slightly academic, but a greater emphasis is placed on physical technique and competition than on scholarly research. This essay is one of the few pieces of academic work required in the curriculum. ', LLM = 'GPT4' WHERE SessionID = 351



Select * FROM StudyResults where SessionID in (430,431)
Select * FROM StudyResults where PreviousSession = 412
Select * FROM PilotStudyResults where SessionID = 353
Select * FROM StudyResults where SessionID = 445

UPDATE StudyResults SET DocQA = NULL, DocBaseline = NULL where SessionID = 445

Select * from PromptLog where sessionid = 445
Delete PromptLog where sessionid = 445 and promptNum = 4
Delete PromptLog where sessionid = 432

UPDATE PromptLog set prompt = NULL, promptTime = NULL where sessionid = 432

exec ReserveSessionID



UPDATE StudyResults SET OverallPreference = -3, UsefulnessPreference = -3, DocBaselineFeedback = 'TestBaseline', DocQAFeedback = 'TestQA' WHERE SessionID = 365


ALTER TABLE StudyResults ADD OverallPreference2 INT NULL, UsefulnessPreference2 INT NULL, DocQAFeedback2 VARCHAR(MAX) NULL, DocBaselineFeedback2 VARCHAR(MAX) NULL
ALTER TABLE StudyResults ADD PreviousSession INT NULL
ALTER TABLE StudyResults ADD ExitMadeMeThink INT NULL
ALTER TABLE StudyResults ADD BadData BIT NULL


INSERT INTO StudyResults (SessionID, ConsentSigned, PreviousSession, Age, Gender, ExperienceLevel, EnglishPrimary) VALUES (402,'2024-03-26 06:08:32',382,35,'Female',2,'Y')