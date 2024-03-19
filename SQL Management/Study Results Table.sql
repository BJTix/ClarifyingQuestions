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

    --Document Preferences
    OverallPreference INT,
    UsefulnessPreference INT,
    Doc1Feedback VARCHAR(MAX),
    Doc2Feedback VARCHAR(MAX),

    --Document Revisions
    RevisionPromptD1R1 VARCHAR(MAX),
    RevisionPromptD1R2 VARCHAR(MAX),
    RevisionPromptD1R3 VARCHAR(MAX),
    
    RevisionPromptD2R1 VARCHAR(MAX),
    RevisionPromptD2R2 VARCHAR(MAX),
    RevisionPromptD2R3 VARCHAR(MAX),

    RevisedDocD1R1 VARCHAR(MAX),
    RevisedDocD1R2 VARCHAR(MAX),
    RevisedDocD1R3 VARCHAR(MAX),

    RevisedDocD2R1 VARCHAR(MAX),
    RevisedDocD2R2 VARCHAR(MAX),
    RevisedDocD2R3 VARCHAR(MAX),

    --Exit Survey
    ExitAnnoying INT,
    ExitEngaged INT,
    ExitWilling INT,
    ExitTwoOptions INT,
    ExitFeedback VARCHAR(MAX),
    CompletedAt DATETIME
)