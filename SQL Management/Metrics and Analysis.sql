--Metrics:
Select 
    total = COUNT(1),
    preferQA = SUM(CASE WHEN 0 < OverallPreference THEN 1 ELSE 0 END),
    preferBaseline = SUM(CASE WHEN OverallPreference < 0 THEN 1 ELSE 0 END),
    preferQAuse = SUM(CASE WHEN 0 < UsefulnessPreference THEN 1 ELSE 0 END),
    preferBaselineUse = SUM(CASE WHEN UsefulnessPreference < 0 THEN 1 ELSE 0 END),
    RefinedQA = SUM(CASE WHEN RevisedDocQA1 is not null THEN 1 ELSE 0 END),
    RefinedBaseline = SUM(CASE WHEN RevisedDocBaseline1 is not null THEN 1 ELSE 0 END),
    preferQARef = SUM(CASE WHEN 0 < OverallPreference2 THEN 1 ELSE 0 END),
    preferBaselineRef = SUM(CASE WHEN OverallPreference2 < 0 THEN 1 ELSE 0 END),
    preferQAUseRef = SUM(CASE WHEN 0 < UsefulnessPreference2 THEN 1 ELSE 0 END),
    preferBaselineUseRef = SUM(CASE WHEN UsefulnessPreference2 < 0 THEN 1 ELSE 0 END)
FROM StudyResults 
where CompletedAt is not NULL
    AND isNULL(BadData,0) = 0

SELECT * FROM StudyResults 
where CompletedAt is not NULL
    AND isNULL(BadData,0) = 0
