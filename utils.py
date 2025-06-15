import json
import pandas as pd
import gspread
import streamlit as st
from google.oauth2 import service_account
import base64

@st.cache_data(ttl=600)
def load_data(selected_sheet):
    # Load service account credentials from Streamlit secrets
    encoded_credentials = st.secrets["GOOGLE_CREDENTIALS_BASE64"]
    credentials_info = json.loads(base64.b64decode(encoded_credentials).decode('utf-8'))
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    
    # Authorize gspread
    client = gspread.authorize(credentials)

    # Open your Google Sheet
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1sjfGn--p6WGLPpsE5TdvNSHiuoFyy7IT6ACwlsRgwgg/edit?usp=sharing")

    # Load selected sheet dynamically
    worksheet = sheet.worksheet(selected_sheet)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df
