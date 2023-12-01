CREATE TABLE PromptLog (
    sessionid int not NULL,
    promptNum int not NULL,
    promptTime DATETIME2,
    prompt VARCHAR(MAX),
    responseTime DATETIME2,
    response VARCHAR(MAX)
    PRIMARY KEY(sessionid, promptNum)
)
