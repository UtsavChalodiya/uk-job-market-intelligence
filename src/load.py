import json, pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg2://")
engine = create_engine(url)
with open("data/raw/jobs.json", encoding="utf-8") as f:
    jobs = json.load(f)

rows = []
for j in jobs:
    try:
        d = datetime.strptime(j.get("date","").split(" ")[0], "%d/%m/%Y").date() if j.get("date") else None
    except: d = None
    rows.append({
        "job_id": j.get("jobId"),
        "title": j.get("jobTitle"),
        "employer": j.get("employerName"),
        "location": j.get("locationName"),
        "salary_min": j.get("minimumSalary"),
        "salary_max": j.get("maximumSalary"),
        "contract_type": j.get("contractType"),
        "date_posted": d,
        "description": j.get("jobDescription"),
        "url": j.get("jobUrl")
    })

df = pd.DataFrame(rows).drop_duplicates("job_id")

with open("sql/schema.sql") as f:
    with engine.begin() as conn:
        conn.execute(text(f.read()))
        
df.to_sql("jobs_raw", engine, if_exists="append", index=False, method="multi")
print("loaded:", len(df), "unique from", len(jobs))