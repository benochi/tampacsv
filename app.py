import streamlit as st
import sqlite3
import pandas as pd

st.title("Tampa Job Explorer (2024 Combined Data)")

# Load combined data
conn = sqlite3.connect("db/tampa_jobs.db")
df = pd.read_sql_query("SELECT * FROM jobs", conn)

# Sidebar filters
st.sidebar.header("Filter Options")
min_wage = st.sidebar.slider("Minimum Hourly Wage", 0, 100, 25)
min_openings = st.sidebar.slider("Minimum Annual Openings", 0, 300, 0)
min_growth = st.sidebar.slider("Minimum % Growth", 0.0, 10.0, 0.0)
source_filter = st.sidebar.multiselect("Source", options=df["Source"].unique(), default=df["Source"].unique())

# Apply base filters
filtered = df[df["Regional Mean Wage"] >= min_wage]
filtered = filtered[filtered["Source"].isin(source_filter)]

# Handle optional filters
if "Regional Openings" in df.columns:
    filtered = filtered[filtered["Regional Openings"].fillna(0) >= min_openings]
if "Regional % Growth" in df.columns:
    filtered = filtered[filtered["Regional % Growth"].fillna(0) >= min_growth]

# Display sorted table
st.dataframe(
    filtered.sort_values("Regional Mean Wage", ascending=False).reset_index(drop=True)
)
