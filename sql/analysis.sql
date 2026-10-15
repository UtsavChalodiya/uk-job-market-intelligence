-- Q1: roles most advertised
SELECT title, COUNT(*) AS jobs
FROM jobs_raw GROUP BY title ORDER BY jobs DESC LIMIT 10;

-- Q2: salary where disclosed
SELECT title, COUNT(*) AS jobs,
  COUNT(salary_min) AS with_salary,
  ROUND(AVG((salary_min+salary_max)/2)) AS avg_mid
FROM jobs_raw GROUP BY title ORDER BY avg_mid DESC NULLS LAST;

-- Q3: where hiring + pay
SELECT location, COUNT(*) AS jobs,
  ROUND(AVG((salary_min+salary_max)/2)) AS avg_mid
FROM jobs_raw GROUP BY location ORDER BY jobs DESC LIMIT 10;
