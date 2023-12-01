CREATE TABLE TestIntroMessage (
    pk int not null,
    messageTime DATETIME2,
    introMessage VARCHAR(MAX),
    PRIMARY KEY(pk)
)