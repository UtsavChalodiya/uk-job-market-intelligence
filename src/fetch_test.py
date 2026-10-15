import requests, json

KEY = "81323289-31fc-46ef-9dc6-b0d0a74292ca"
url = "https://www.reed.co.uk/api/1.0/search?keywords=data%20analyst&locationName=London&resultsToTake=5"
r = requests.get(url, auth=(KEY, ""))
data = r.json()

with open("data/raw/test.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("saved, total:", data["totalResults"])