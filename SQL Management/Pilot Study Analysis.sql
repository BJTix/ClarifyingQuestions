SELECT 
    QACloseness = AVG(CAST(QACloseness AS float)),
    QAUsefulness = AVG(CAST(QAUsefulness AS float)),
    QAOverall = AVG(CAST(QAOverall AS float)),
    QAComposite = AVG(CAST(QACloseness AS float) + CAST(QAUsefulness AS float) + CAST(QAOverall AS float)),

    BaselineCloseness = AVG(CAST(BaselineCloseness AS float)),
    BaselineUsefulness = AVG(CAST(BaselineUsefulness AS float)),
    BaselineOverall = AVG(CAST(BaselineOverall AS float)),
    BaselineComposite = AVG(CAST(BaselineCloseness AS float) + CAST(BaselineUsefulness AS float) + CAST(BaselineOverall AS float))
FROM PilotStudyResults

SELECT 
    ExitAnnoying = AVG(CAST(ExitAnnoying AS FLOAT)), 
    ExitEngaged = AVG(CAST(ExitEngaged AS FLOAT)), 
    ExitTwoOptions = AVG(CAST(ExitTwoOptions AS FLOAT)),
    ExitWilling = AVG(CAST(ExitWilling AS FLOAT)),
    ExitComposite = AVG(CAST(ExitEngaged AS FLOAT) + CAST(ExitTwoOptions AS FLOAT) + CAST(ExitWilling AS FLOAT) - CAST(ExitAnnoying AS FLOAT))
FROM PilotStudyResults

SELECT
    ExitFeedback
FROM PilotStudyResults

SELECT
    CompletionTime = AVG(DATEDIFF(second,ConsentSigned,CompletedAt)),
    MinCompletionTime = MIN(DATEDIFF(second,ConsentSigned,CompletedAt)),
    MaxCompletionTime = MAX(DATEDIFF(second,ConsentSigned,CompletedAt))
FROM PilotStudyResults ps

SELECT
    prompt, CompletionTime = CompletedAt - ConsentSigned 
FROM PilotStudyResults ps

SELECT * FROM PilotStudyResults

Select * FROM PromptLog where sessionid  =272

--Preferred which (by study)
SELECT 
    QAComposite = AVG(CAST(QACloseness AS float) + CAST(QAUsefulness AS float) + CAST(QAOverall AS float)),
    BaselineComposite = AVG(CAST(BaselineCloseness AS float) + CAST(BaselineUsefulness AS float) + CAST(BaselineOverall AS float))
FROM PilotStudyResults


select top 100 * from ClarifyingQuestionsData


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