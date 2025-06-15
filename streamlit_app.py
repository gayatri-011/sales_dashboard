import streamlit as st
import json
import base64
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ================== 1️⃣ Load Credentials ==================
encoded_credentials = st.secrets["GOOGLE_CREDENTIALS_BASE64"]
service_account_info = json.loads(base64.b64decode(encoded_credentials).decode('utf-8'))

# ================== 2️⃣ Authorize Google Sheets ==================
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
gc = gspread.authorize(credentials)

# ================== 3️⃣ Open Spreadsheet ==================
spreadsheet_name = "Project Progress Review"
spreadsheet = gc.open(spreadsheet_name)

# ================== 4️⃣ List All Sheets ==================
sheet_list = [ws.title for ws in spreadsheet.worksheets()]
selected_sheet = st.selectbox("Select Sheet", sheet_list)

# ================== 5️⃣ Load Data ==================
worksheet = spreadsheet.worksheet(selected_sheet)
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# ================== 6️⃣ Display Data ==================
st.write(f"**Showing data from sheet:** `{selected_sheet}`")
st.dataframe(df)
