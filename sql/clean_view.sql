DROP VIEW IF EXISTS jobs_clean;
CREATE VIEW jobs_clean AS
SELECT *,
  (salary_min+salary_max)/2 AS salary_mid,
  CASE WHEN salary_min >= 10000 THEN 'annual' ELSE 'other' END AS salary_type
FROM jobs_raw
WHERE (
  LOWER(title) LIKE '%data analyst%' OR LOWER(title) LIKE '%data engineer%'
  OR LOWER(title) LIKE '%data scientist%' OR LOWER(title) LIKE '%bi analyst%'
  OR LOWER(title) LIKE '%business analyst%' OR LOWER(title) LIKE '%machine learning%'
  OR LOWER(title) LIKE '%data architect%' OR LOWER(title) LIKE '%analytics%'
)
AND LOWER(title) NOT LIKE '%trainee%'
AND LOWER(title) NOT LIKE '%no experience%'
AND LOWER(title) NOT LIKE '%job guarantee%'
AND LOWER(title) NOT LIKE '%graduate scheme%'
AND LOWER(title) NOT LIKE '%account manager%'
AND LOWER(title) NOT LIKE '%sales%';