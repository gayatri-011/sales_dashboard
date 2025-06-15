import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Company Summary Report", layout="wide")
st.title("📊 Company Summary Report")

# Load data
df = load_data()

# -------------------- KPIs SECTION --------------------
total_leads = len(df)
converted_leads = len(df[df["Stage Group"] == "Converted"])
in_progress_leads = len(df[df["Stage Group"] == "In Progress"])
conversion_rate = round((converted_leads / total_leads) * 100, 1) if total_leads > 0 else 0

st.header("Overall KPIs")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Leads", total_leads)
kpi2.metric("Converted", converted_leads)
kpi3.metric("In Progress", in_progress_leads)
kpi4.metric("Conversion %", f"{conversion_rate}%")

# -------------------- DATA PREPARATION --------------------

# Lead Quality (In Progress)
lead_quality_progress = (
    df[df["Stage Group"] == "In Progress"]
    .groupby("Lead Quality")
    .size()
    .reset_index(name="Count")
    .sort_values(by="Count", ascending=False)
)

# Month-wise Progress
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

# -------------------- CHARTS SECTION --------------------
st.header("Detailed Visualizations")

# Divide into 2 columns for better layout
col_left, col_right = st.columns(2)

# ---- Left Chart (Lead Quality Breakdown) ----
with col_left:
    st.subheader("Lead Quality Breakdown (In Progress)")
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    bars = ax1.bar(lead_quality_progress["Lead Quality"], lead_quality_progress["Count"], color="#2196f3")
    ax1.bar_label(bars, padding=3)
    ax1.set_xlabel("Lead Quality Category")
    ax1.set_ylabel("Number of In-Progress Leads")
    plt.xticks(rotation=0)
    st.pyplot(fig1)

# ---- Right Chart (Month-wise Progress) ----
with col_right:
    st.subheader("Month-wise Progress")
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    month_pivot.plot(
        x="Month",
        kind="bar",
        stacked=True,
        color=["#4caf50", "#ff9800", "#f44336"],
        ax=ax2
    )

    for container in ax2.containers:
        ax2.bar_label(container, label_type='center', fontsize=8)
    
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Number of Leads")
    plt.xticks(rotation=0)
    st.pyplot(fig2)
