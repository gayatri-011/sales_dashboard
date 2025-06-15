import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Owner Wise Dashboard", layout="wide")

df = load_data()

all_owners = sorted(df["Owner"].unique().tolist())

selected_owner = st.selectbox("Select Owner", all_owners)

df_owner = df[df["Owner"] == selected_owner]

st.title(f"📊 Report for {selected_owner}")

total_leads = len(df_owner)
converted = len(df_owner[df_owner["Stage Group"] == "Converted"])
in_progress = len(df_owner[df_owner["Stage Group"] == "In Progress"])
not_converted = len(df_owner[df_owner["Stage Group"] == "Not Converted"])
conversion_rate = (converted / total_leads) * 100 if total_leads > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", total_leads)
col2.metric("Converted", converted)
col3.metric("In Progress", in_progress)
col4.metric("Conversion %", f"{conversion_rate:.1f}%")

st.divider()

st.subheader("Lead Quality Breakdown (In Progress)")
lead_quality_progress = pd.pivot_table(
    df_owner[df_owner["Stage Group"] == "In Progress"],
    index="Lead Quality",
    aggfunc="size",
    fill_value=0
)
st.dataframe(lead_quality_progress)

st.divider()

st.subheader("Month-wise Progress")
month_pivot = pd.pivot_table(
    df_owner,
    index="Month",
    columns="Stage Group",
    aggfunc="size",
    fill_value=0
).sort_index(ascending=False)

st.dataframe(month_pivot)
