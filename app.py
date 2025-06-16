import streamlit as st
import sqlite3
import pandas as pd

st.title("Tampa Job Explorer (2024–25)")

# Load data from SQLite
conn = sqlite3.connect("db/tampa_jobs.db")
df = pd.read_sql_query("SELECT * FROM jobs", conn)

# Sidebar filters
min_wage = st.sidebar.slider("Min Hourly Wage", 0, 100, 25)
min_openings = st.sidebar.slider("Min Annual Openings", 0, 300, 50)
min_growth = st.sidebar.slider("Min % Growth", 0.0, 5.0, 1.0)

filtered = df[
    (df["2022 Hourly Wage Mean"] >= min_wage) &
    (df["Regional Annual Openings"] >= min_openings) &
    (df["Regional % Growth"] >= min_growth)
]

st.dataframe(filtered.sort_values("2022 Hourly Wage Mean", ascending=False))
