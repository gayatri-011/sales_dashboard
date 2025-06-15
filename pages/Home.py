import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Company Summary Report", layout="wide")
st.title("📊 Company Summary Report")

# Load data
df = load_data()

# -------------------- KPI SECTION --------------------
total_leads = len(df)
converted_leads = len(df[df["Stage Group"] == "Converted"])
in_progress_leads = len(df[df["Stage Group"] == "In Progress"])
conversion_rate = round((converted_leads / total_leads) * 100, 1) if total_leads > 0 else 0

st.header("Overall KPIs")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", total_leads)
col2.metric("Converted", converted_leads)
col3.metric("In Progress", in_progress_leads)
col4.metric("Conversion %", f"{conversion_rate}%")

# -------------------- LEAD QUALITY CHART --------------------
lead_quality_progress = (
    df[df["Stage Group"] == "In Progress"]
    .groupby("Lead Quality")
    .size()
    .reset_index(name="Count")
    .sort_values(by="Count", ascending=False)
)

st.subheader("📊 Lead Quality Breakdown (In Progress)")

fig1, ax1 = plt.subplots(figsize=(6, 4))
plt.bar(lead_quality_progress["Lead Quality"], lead_quality_progress["Count"], color="#2196f3")
plt.ylabel("Count")
plt.xticks(rotation=0)
st.pyplot(fig1)

# -------------------- MONTH-WISE PROGRESS CHART --------------------
month_pivot = (
    df.groupby(["Month", "Stage Group"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
    .sort_values(by="Month", ascending=True)
)
month_pivot = month_pivot.rename(
    columns={
        "Converted": "Converted",
        "In Progress": "In Progress",
        "Not Converted": "Not Converted",
    }
)

st.subheader("📈 Month-wise Progress")

fig2, ax2 = plt.subplots(figsize=(8, 5))
month_pivot.plot(
    x="Month",
    kind="bar",
    stacked=True,
    color=["#4caf50", "#ff9800", "#f44336"],
    ax=ax2,
)
plt.ylabel("Number of Leads")
plt.xlabel("Month")
plt.xticks(rotation=0)
st.pyplot(fig2)
