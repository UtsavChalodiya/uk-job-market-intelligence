import json
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import insert

load_dotenv()


def get_engine():
    """Create a PostgreSQL engine from the local environment."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Add your PostgreSQL connection string to .env."
        )

    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )

    return create_engine(database_url)


def parse_posted_date(value):
    """Parse Reed's date format; return None when it is missing or invalid."""
    if not value:
        return None
    try:
        return datetime.strptime(value.split(" ")[0], "%d/%m/%Y").date()
    except ValueError:
        return None


def main():
    """Load the local job snapshot, inserting new IDs and updating existing IDs."""
    with open("data/raw/jobs.json", encoding="utf-8") as input_file:
        jobs = json.load(input_file)

    rows = []
    for job in jobs:
        job_id = job.get("jobId")
        if job_id is None:
            continue

        rows.append(
            {
                "job_id": job_id,
                "title": job.get("jobTitle"),
                "employer": job.get("employerName"),
                "location": job.get("locationName"),
                "salary_min": job.get("minimumSalary"),
                "salary_max": job.get("maximumSalary"),
                "contract_type": job.get("contractType"),
                "date_posted": parse_posted_date(job.get("date")),
                "description": job.get("jobDescription"),
                "url": job.get("jobUrl"),
            }
        )

    df = pd.DataFrame(rows).drop_duplicates("job_id")
    if df.empty:
        print("No listings with a valid job ID were found; nothing to load.")
        return

    engine = get_engine()
    metadata = MetaData()
    jobs_table = Table("jobs_raw", metadata, autoload_with=engine)

    records = df.to_dict(orient="records")
    update_columns = {
        column.name: getattr(insert(jobs_table).excluded, column.name)
        for column in jobs_table.columns
        if column.name != "job_id"
    }

    with engine.begin() as connection:
        for start in range(0, len(records), 500):
            batch = records[start : start + 500]
            statement = insert(jobs_table).values(batch)
            statement = statement.on_conflict_do_update(
                index_elements=["job_id"],
                set_=update_columns,
            )
            connection.execute(statement)

    print(f"Upserted {len(df)} unique listings from {len(jobs)} API records.")


if __name__ == "__main__":
    main()
