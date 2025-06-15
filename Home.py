import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Company Dashboard", layout="wide")
st.title("📊 Company Summary Report")

df = load_data()

st.subheader("Overall KPIs")

total_leads = len(df)
converted = len(df[df["Stage Group"] == "Converted"])
in_progress = len(df[df["Stage Group"] == "In Progress"])
not_converted = len(df[df["Stage Group"] == "Not Converted"])
conversion_rate = (converted / total_leads) * 100 if total_leads > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", total_leads)
col2.metric("Converted", converted)
col3.metric("In Progress", in_progress)
col4.metric("Conversion %", f"{conversion_rate:.1f}%")

st.divider()

st.subheader("Lead Quality Breakdown (In Progress)")
lead_quality_progress = pd.pivot_table(
    df[df["Stage Group"] == "In Progress"],
    index="Lead Quality",
    aggfunc="size",
    fill_value=0
)
st.dataframe(lead_quality_progress)

st.divider()

st.subheader("Month-wise Progress")
month_pivot = pd.pivot_table(
    df,
    index="Month",
    columns="Stage Group",
    aggfunc="size",
    fill_value=0
).sort_index(ascending=False)

st.dataframe(month_pivot)
