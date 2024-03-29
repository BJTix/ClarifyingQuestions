CREATE TABLE StudyResults (
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
    QuestionsFeedback VARCHAR(MAX),

    --Documents
    DocBaseline VARCHAR(MAX),
    DocQA VARCHAR(MAX),
    ShowQAFirst BIT,
    LLM VARCHAR(10),

    --Document Preferences
    OverallPreference INT,
    UsefulnessPreference INT,
    DocQAFeedback VARCHAR(MAX),
    DocBaselineFeedback VARCHAR(MAX),

    --Document Revisions
    RevisionPromptQA1 VARCHAR(MAX),
    RevisionPromptQA2 VARCHAR(MAX),
    RevisionPromptQA3 VARCHAR(MAX),
    
    RevisionPromptBaseline1 VARCHAR(MAX),
    RevisionPromptBaseline2 VARCHAR(MAX),
    RevisionPromptBaseline3 VARCHAR(MAX),

    RevisedDocQA1 VARCHAR(MAX),
    RevisedDocQA2 VARCHAR(MAX),
    RevisedDocQA3 VARCHAR(MAX),

    RevisedDocBaseline1 VARCHAR(MAX),
    RevisedDocBaseline2 VARCHAR(MAX),
    RevisedDocBaseline3 VARCHAR(MAX),

    --Revised Preferences:
    OverallPreference2 INT NULL, 
    UsefulnessPreference2 INT NULL, 
    DocQAFeedback2 VARCHAR(MAX) NULL, 
    DocBaselineFeedback2 VARCHAR(MAX) NULL,

    --Exit Survey
    ExitAnnoying INT,
    ExitEngaged INT,
    ExitWilling INT,
    ExitTwoOptions INT,
    ExitFeedback VARCHAR(MAX),
    CompletedAt DATETIME
)