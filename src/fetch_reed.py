import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("REED_API_KEY")
BASE_URL = "https://www.reed.co.uk/api/1.0/search"
KEYWORDS = ["data analyst", "data engineer", "data scientist"]
PAGE_SIZE = 100
MAX_RESULTS_PER_KEYWORD = 300
REQUEST_TIMEOUT = 30


def fetch_jobs():
    """Fetch UK data-job listings from Reed using an API key in the environment."""
    if not API_KEY:
        raise RuntimeError(
            "REED_API_KEY is not set. Add it to your local .env file; "
            "never hardcode API credentials in source code."
        )

    session = requests.Session()
    jobs_by_id = {}

    for keyword in KEYWORDS:
        for offset in range(0, MAX_RESULTS_PER_KEYWORD, PAGE_SIZE):
            params = {
                "keywords": keyword,
                "locationName": "UK",
                "resultsToTake": PAGE_SIZE,
                "resultsToSkip": offset,
            }
            response = session.get(
                BASE_URL,
                auth=(API_KEY, ""),
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
            batch = payload.get("results", [])

            print(f"{keyword} | offset {offset} | retrieved {len(batch)}")

            for job in batch:
                job_id = job.get("jobId")
                if job_id is not None:
                    jobs_by_id[job_id] = job

            if len(batch) < PAGE_SIZE:
                break

            time.sleep(1)

    return list(jobs_by_id.values())


def main():
    """Fetch listings and save a deduplicated JSON snapshot."""
    jobs = fetch_jobs()
    output_path = Path("data/raw/jobs.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(jobs, output_file, indent=2, ensure_ascii=False)

    print(f"Saved {len(jobs)} unique listings to {output_path}")


if __name__ == "__main__":
    main()
