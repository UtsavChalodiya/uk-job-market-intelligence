import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
load_dotenv()
url = os.getenv("DATABASE_URL").replace("postgresql://","postgresql+psycopg2://")
engine = create_engine(url)

with open("sql/clean_view.sql") as f:
    with engine.begin() as c:
        c.execute(text(f.read()))
print("view created")

queries = [
  "SELECT COUNT(*) FROM jobs_raw",
  "SELECT COUNT(*) FROM jobs_clean",
  "SELECT title, COUNT(*) jobs, ROUND(AVG(salary_mid)) avg_pay FROM jobs_clean WHERE salary_type='annual' AND salary_mid BETWEEN 15000 AND 200000 GROUP BY title ORDER BY jobs DESC LIMIT 10"
]

with engine.connect() as c:
    for q in queries:
        print("\n>>", q[:60])
        for row in c.execute(text(q)):
            print(row)