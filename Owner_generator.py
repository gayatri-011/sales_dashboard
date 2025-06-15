import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

# Load data directly from Google Sheets (same as utils.py logic)
def load_data():
    creds_dict = {
        "type": os.environ["type"],
        "project_id": os.environ["project_id"],
        "private_key_id": os.environ["private_key_id"],
        "private_key": os.environ["private_key"].replace("\\n", "\n"),
        "client_email": os.environ["client_email"],
        "client_id": os.environ["client_id"],
        "auth_uri": os.environ["auth_uri"],
        "token_uri": os.environ["token_uri"],
        "auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
        "client_x509_cert_url": os.environ["client_x509_cert_url"]
    }

    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)

    SHEET_URL = os.environ["sheet_url"]
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

# Generate Owner Files
def generate_owner_pages():
    df = load_data()

    owners = df["Owner"].unique()

    for owner in owners:
        safe_owner = owner.replace(" ", "_").replace("/", "_")
        filename = f"pages/Owner_{safe_owner}.py"

        with open(filename, "w") as f:
            f.write(f'import streamlit as st\n')
            f.write(f'import pandas as pd\n')
            f.write(f'import matplotlib.pyplot as plt\n')
            f.write(f'from utils import load_data\n\n')
            f.write(f'df = load_data()\n')
            f.write(f'df = df[df["Owner"] == "{owner}"]\n\n')
            # (HERE WE WILL COPY EXACT SAME LOGIC FROM Home.py INTO EACH OWNER FILE)
