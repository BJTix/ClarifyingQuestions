CREATE TABLE PilotStudyResults (
    SessionID INT NOT NULL PRIMARY KEY,
    ConsentSigned DATETIME,

    --Demographics Screen:
    Age INT,
    Gender VARCHAR(10),
    ExperienceLevel INT,
    EnglishPrimary VARCHAR(1),

    --Prompt and discussion
    Prompt VARCHAR(MAX),
    Q1 VARCHAR(MAX),
    A1  VARCHAR(MAX),
    Q2 VARCHAR(MAX),
    A2 VARCHAR(MAX),
    Q3 VARCHAR(MAX),
    A3 VARCHAR(MAX),

    --Documents
    DocBaseline VARCHAR(MAX),
    DocQA VARCHAR(MAX),
    ShowQAFirst BIT,

    --Ratings for Baseline
    BaselineCloseness INT,
    BaselineUsefulness INT,
    BaselineOverall INT,

    --Ratings for QA Doc
    QACloseness INT,
    QAUsefulness INT,
    QAOverall INT,
    
    --Exit Survey
    ExitAnnoying INT,
    ExitEngaged INT,
    ExitWilling INT,
    ExitTwoOptions INT,
    ExitFeedback VARCHAR(MAX),
    CompletedAt DATETIME
)