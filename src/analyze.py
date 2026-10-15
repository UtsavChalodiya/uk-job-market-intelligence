import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
load_dotenv()
url = os.getenv("DATABASE_URL").replace("postgresql://","postgresql+psycopg2://")
engine = create_engine(url)
with open("sql/analysis.sql") as f:
    queries = f.read().split(";")
    for q in queries:
        if q.strip():
            print("\n>>", q.strip()[:60])
            with engine.connect() as c:
                for row in c.execute(text(q)):
                    print(row)