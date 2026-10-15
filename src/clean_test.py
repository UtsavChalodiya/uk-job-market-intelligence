import json, pandas as pd

with open("data/raw/test.json", encoding="utf-8") as f:
    data = json.load(f)["results"]

df = pd.DataFrame(data)
print(df[["jobTitle","locationName","minimumSalary","maximumSalary"]])

# 1. salary_mid, keep nulls for now
df["salary_mid"] = (df["minimumSalary"] + df["maximumSalary"]) / 2
# 2. flag missing salary
print("\nmissing salary:", df["salary_mid"].isna().sum(), "/", len(df))
# 3. simple skill flag
df["mentions_sql"] = df["jobDescription"].str.lower().str.contains("sql", na=False)
print(df[["jobTitle","salary_mid","mentions_sql"]])