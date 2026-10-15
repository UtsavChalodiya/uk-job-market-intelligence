import requests, json, time

KEY = "81323289-31fc-46ef-9dc6-b0d0a74292ca"
BASE = "https://www.reed.co.uk/api/1.0/search"

keywords = ["data analyst", "data engineer", "data scientist"]
all_jobs = []

for kw in keywords:
    for skip in [0, 100, 200]:
        params = {"keywords": kw, "locationName": "UK", "resultsToTake": 100, "resultsToSkip": skip}
        r = requests.get(BASE, auth=(KEY, ""), params=params)
        batch = r.json()["results"]
        print(kw, skip, "got", len(batch))
        all_jobs.extend(batch)
        time.sleep(1)  # be polite, don't hammer API

with open("data/raw/jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2)

print("total saved:", len(all_jobs))