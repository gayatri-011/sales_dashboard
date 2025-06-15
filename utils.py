import json
import pandas as pd
import gspread
import streamlit as st
from google.oauth2 import service_account

@st.cache_data(ttl=600)
def load_data(selected_sheet):
    # Load service account credentials directly from Streamlit secrets
    credentials_info = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    
    # Authorize gspread
    client = gspread.authorize(credentials)

    # Open your Google Sheet
    sheet = client.open("Monthly Analysis and Prediction")

    # Load selected sheet dynamically
    worksheet = sheet.worksheet(selected_sheet)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df
