Users: graduates, recruiters, career advisers

Problem: No clear view of which skills/locations pay more for UK data jobs

Questions this answers:

1. Which data roles are most advertised?
2. Which skills drive higher salaries?
3. Where are companies hiring and where is pay highest?
4. How do salary and role differ for full-time vs contract?
5. What changes month-to-month?



Data: Reed.co.uk API (permitted)

Stack: Python -> Cloud Postgres -> SQL -> Power BI



Pipeline:

Reed API -> data/raw/jobs.json (528 saved, 397 unique) -> jobs\_raw -> jobs\_clean view -> Power BI on jobs\_clean



Cleaning:

\- Dedupe by job\_id

\- Title filter (fix %ai% -> trainee bug) + exclude training spam

\- salary\_type=annual only (salary\_min>=10000), range 15k-200k



Current findings:

\- Data Engineer \~£50k, Lead £80k+

\- add your 2 more lines from analyze\_clean output



Reproduce:

pip install -r requirements.txt

python src/fetch\_reed.py

python src/load.py

python src/analyze\_clean.py



Source: Reed.co.uk Jobseeker API.

Status: Power BI dashboard in progress in powerbi/.

