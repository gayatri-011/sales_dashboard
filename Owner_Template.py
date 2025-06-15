import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Owner Performance", layout="wide")

# Load data
df = load_data()

# OWNER FILTER (auto-applied when you generate file per owner)
owner_name = "PUT_OWNER_NAME_HERE"
df = df[df["Owner"] == owner_name]

st.title(f"📊 Report for {owner_name}")

# -------------------- KPIs --------------------
total_leads = len(df)
converted_leads = len(df[df["Stage Group"] == "Converted"])
in_progress_leads = len(df[df["Stage Group"] == "In Progress"])
conversion_rate = round((converted_leads / total_leads) * 100, 1) if total_leads > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Leads", total_leads)
k2.metric("Converted", converted_leads)
k3.metric("In Progress", in_progress_leads)
k4.metric("Conversion %", f"{conversion_rate}%")

# -------------------- CHARTS --------------------
st.header("Detailed Visualizations")
col_left, col_mid, col_right = st.columns(3)

# Lead Quality Chart
with col_left:
    st.subheader("Lead Quality Breakdown (In Progress)")
    lead_quality = (
        df[df["Stage Group"] == "In Progress"]
        .groupby("Lead Quality")
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
    )
    max_count = lead_quality["Count"].max()
    y_limit = round(max_count * 1.2, -1)

    fig1, ax1 = plt.subplots(figsize=(4, 3))
    bars = ax1.bar(lead_quality["Lead Quality"], lead_quality["Count"], color="#4682B4")
    ax1.bar_label(bars, padding=3)
    ax1.set_xlabel("Lead Quality")
    ax1.set_ylabel("In Progress Leads")
    plt.ylim(0, y_limit)
    plt.xticks(rotation=0)
    st.pyplot(fig1)

# Conversion Rate Chart
with col_mid:
    st.subheader("Month-wise Conversion Rate")
    conversion_rate_df = (
        df.groupby("Month")
        .agg(Total=("Stage Group", "count"),
             Converted=("Stage Group", lambda x: (x == "Converted").sum()))
    ).reset_index()

    conversion_rate_df["Conversion Rate"] = (conversion_rate_df["Converted"] / conversion_rate_df["Total"]) * 100

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    conversion_rate_df["Month"] = pd.Categorical(conversion_rate_df["Month"], categories=month_order, ordered=True)
    conversion_rate_df = conversion_rate_df.sort_values("Month")

    max_rate = conversion_rate_df["Conversion Rate"].max()
    upper_limit = max(5, round(max_rate + 1))

    fig2, ax2 = plt.subplots(figsize=(4, 3))
    bars = ax2.bar(conversion_rate_df["Month"], conversion_rate_df["Conversion Rate"], color="#4682B4")
    ax2.bar_label(bars, fmt='%.1f%%', padding=3)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Conversion Rate (%)")
    plt.ylim(0, upper_limit)
    plt.xticks(rotation=0)
    st.pyplot(fig2)

# Stagnant Leads Chart
with col_right:
    st.subheader("Stagnant Leads")
    stagnant_counts = {
        "<= 30 days": (df["Days Since Last Update"] <= 30).sum(),
        "> 30 days": (df["Days Since Last Update"] > 30).sum()
    }
    stagnant_df = pd.DataFrame(list(stagnant_counts.items()), columns=["Category", "Count"])
    max_stagnant = stagnant_df["Count"].max()
    y_limit_stag = round(max_stagnant * 1.2, -1)

    fig3, ax3 = plt.subplots(figsize=(4, 3))
    bars = ax3.bar(stagnant_df["Category"], stagnant_df["Count"], color="#4682B4")
    ax3.bar_label(bars, padding=3)
    ax3.set_xlabel("Lead Update Status")
    ax3.set_ylabel("Number of Leads")
    plt.ylim(0, y_limit_stag)
    plt.xticks(rotation=0)
    st.pyplot(fig3)
