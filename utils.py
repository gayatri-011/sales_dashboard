import json
import gspread
import pandas as pd
from google.oauth2 import service_account

def load_data(sheet_name):
    # Load credentials from local file
    with open('service_account.json') as f:
        service_account_info = json.load(f)

    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes)

    client = gspread.authorize(credentials)

    # Load data from Google Sheet
    sheet = client.open("Monthly Analysis and Prediction")
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df
