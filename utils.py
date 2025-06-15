import json
import pandas as pd
import gspread
import streamlit as st
from google.oauth2 import service_account

# Caching data load to reduce API calls
@st.cache_data(ttl=600)
def load_data():
    # Load service account credentials from Streamlit secrets
    credentials_info = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = gspread.authorize(credentials)

    # Open your Google Sheet
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1sjfGn--p6WGLPpsE5TdvNSHiuoFyy7IT6ACwlsRgwgg/edit?usp=sharing")

    # Load both March and April sheets
    data_apr = sheet.worksheet("Cleaned_April").get_all_records()
    df_apr = pd.DataFrame(data_apr)

    data_mar = sheet.worksheet("Cleaned_March").get_all_records()
    df_mar = pd.DataFrame(data_mar)

    # Combine both months
    df_all = pd.concat([df_apr, df_mar], ignore_index=True)
    
    return df_all
