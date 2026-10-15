CREATE TABLE IF NOT EXISTS jobs_raw (
  job_id BIGINT PRIMARY KEY,
  title TEXT,
  employer TEXT,
  location TEXT,
  salary_min NUMERIC,
  salary_max NUMERIC,
  contract_type TEXT,
  date_posted DATE,
  description TEXT,
  url TEXT
);