import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }

    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)

    SHEET_URL = st.secrets["sheet_url"]
    spreadsheet = gc.open_by_url(SHEET_URL)

    all_worksheets = spreadsheet.worksheets()
    dataframes = []

    for ws in all_worksheets:
        if ws.title.startswith("Cleaned_"):
            temp_data = ws.get_all_records()
            df_temp = pd.DataFrame(temp_data)
            month_name = ws.title.replace("Cleaned_", "")
            df_temp["Month"] = month_name
            dataframes.append(df_temp)

    df = pd.concat(dataframes, ignore_index=True)

    for col in ["Lead Quality", "Stage Group", "Destinations"]:
        if col in df.columns:
            df[col].replace("", "Unknown", inplace=True)
            df[col].fillna("Unknown", inplace=True)

    return df
