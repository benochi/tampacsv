import pandas as pd
import sqlite3
from pathlib import Path

# Paths
root = Path(__file__).resolve().parents[1]
db_path = root / "db" / "tampa_jobs.db"
rdol_path = root / "data" / "rdol_all_2425.xlsx"
tampa2024_path = root / "data" / "2024_tampa.xlsx"

# --- Load RDOL ---
df1_raw = pd.read_excel(rdol_path, sheet_name="WDA10 DOL", skiprows=11)
df1_raw.columns = df1_raw.iloc[2]
df1 = df1_raw.iloc[4:].copy()
df1 = df1[df1["Occupation Title*"].notna()]
df1.columns = df1.columns.astype(str).str.strip()
df1.columns = [
    "SOC Code", "HSHW", "Occupation Title",
    "Regional % Growth", "Regional Openings", "Regional Mean Wage", "Regional Entry Wage",
    "Statewide % Growth", "Statewide Openings", "Statewide Mean Wage", "Statewide Entry Wage",
    "Training Code", "Target Industry", "Education Level"
]
df1["Source"] = "2024–25"
df1_subset = df1[[
    "SOC Code", "Occupation Title", "Regional Mean Wage", "Regional Entry Wage",
    "Regional % Growth", "Regional Openings", "Source"
]]

# --- Load Tampa with hardcoded columns ---
columns = [
    "SOC Code", "Occupation Title", "Employment", "Mean Wage", "Median",
    "Entry Wage", "Experienced", "P10", "P25", "P75", "P90"
]
df2 = pd.read_excel(
    tampa2024_path,
    sheet_name="Tampa-St. Petersburg-Clearwater",
    skiprows=6,
    header=None,
    names=columns
)

df2["Source"] = "2024"
df2 = df2[df2["SOC Code"].notna() & df2["Occupation Title"].notna()]

df2_subset = df2[["SOC Code", "Occupation Title", "Mean Wage", "Entry Wage", "Source"]].copy()
df2_subset = df2_subset.rename(columns={
    "Mean Wage": "Regional Mean Wage",
    "Entry Wage": "Regional Entry Wage"
})
df2_subset["Regional % Growth"] = None
df2_subset["Regional Openings"] = None

# Combine
cols = [
    "SOC Code", "Occupation Title", "Regional Mean Wage", "Regional Entry Wage",
    "Regional % Growth", "Regional Openings", "Source"
]
df_combined = pd.concat([df1_subset[cols], df2_subset[cols]], ignore_index=True)

# Convert to numeric
for col in ["Regional Mean Wage", "Regional Entry Wage", "Regional % Growth", "Regional Openings"]:
    df_combined[col] = pd.to_numeric(df_combined[col], errors="coerce")

# Save to SQLite
db_path.parent.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(db_path) as conn:
    conn.execute("DROP TABLE IF EXISTS jobs")
    df_combined.to_sql("jobs", conn, if_exists="replace", index=False)

print(f"Saved to {db_path}")
