import pandas as pd
import sqlite3

# Load and clean the Excel data
df = pd.read_excel("data/rdol_all_2425.xlsx", sheet_name="WDA10 DOL", skiprows=11)
df.columns = df.iloc[2]
df = df.iloc[4:]
df = df[df["Occupation Title*"].notna()]
df["Regional Annual Openings"] = pd.to_numeric(df["Regional Annual Openings"], errors="coerce")
df["2022 Hourly Wage Mean"] = pd.to_numeric(df["2022 Hourly Wage Mean"], errors="coerce")
df["Regional % Growth"] = pd.to_numeric(df["Regional % Growth"], errors="coerce")

# Save to SQLite
conn = sqlite3.connect("db/tampa_jobs.db")
df.to_sql("jobs", conn, if_exists="replace", index=False)
conn.close()

print("Data ingested into db/tampa_jobs.db")
