import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Company Summary Report", layout="wide")
st.title("📊 Company Summary Report")

# Load data
df = load_data()

# Month-wise Progress Table
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

st.subheader("Month-wise Progress")
st.dataframe(month_pivot)

# 🔧 Chart 1: Month-wise Progress (Stacked Bar Chart)
st.subheader("📈 Month-wise Progress Chart")

fig1, ax1 = plt.subplots(figsize=(8, 5))
month_pivot.plot(
    x="Month",
    kind="bar",
    stacked=True,
    color=["#4caf50", "#ff9800", "#f44336"],
    ax=ax1,
)
plt.ylabel("Number of Leads")
plt.xlabel("Month")
plt.xticks(rotation=0)
st.pyplot(fig1)

# Lead Quality Breakdown (In Progress only)
lead_quality_progress = (
    df[df["Stage Group"] == "In Progress"]
    .groupby("Lead Quality")
    .size()
    .reset_index(name="Count")
    .sort_values(by="Count", ascending=False)
)

st.subheader("Lead Quality Breakdown (In Progress)")
st.dataframe(lead_quality_progress)

# 🔧 Chart 2: Lead Quality Breakdown (Bar Chart)
st.subheader("📊 Lead Quality Breakdown Chart")

fig2, ax2 = plt.subplots(figsize=(6, 4))
plt.bar(lead_quality_progress["Lead Quality"], lead_quality_progress["Count"], color="#2196f3")
plt.ylabel("Count")
plt.xticks(rotation=0)
st.pyplot(fig2)
