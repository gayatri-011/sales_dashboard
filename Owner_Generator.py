import os
import pandas as pd
import gspread
from string import Template
from google.oauth2.service_account import Credentials

# Google Sheets Auth
SERVICE_ACCOUNT_FILE = "service_account.json"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=scope)
gc = gspread.authorize(credentials)

# Fetch data from Google Sheet
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1sjfGn--p6WGLPpsE5TdvNSHiuoFyy7IT6ACwlsRgwgg"
spreadsheet = gc.open_by_url(SPREADSHEET_URL)

# Read all Cleaned sheets
all_worksheets = spreadsheet.worksheets()
dataframes = []

for ws in all_worksheets:
    if ws.title.startswith("Cleaned_"):
        temp_data = ws.get_all_records()
        df_temp = pd.DataFrame(temp_data)
        dataframes.append(df_temp)

df = pd.concat(dataframes, ignore_index=True)

# Load template
with open("Owner_Template.py", "r") as f:
    template_content = f.read()

# Create pages directory if not exists
if not os.path.exists("pages"):
    os.makedirs("pages")

# Get all unique owners
owners = df["Owner"].dropna().unique()

# Generate one page per owner
for owner in owners:
    safe_owner = owner.replace(" ", "_").replace("/", "_")
    filename = f"pages/Owner_{safe_owner}.py"

    # Substitute template with owner name
    template = Template(template_content)
    content = template.substitute(owner=owner)

    # Write to file
    with open(filename, "w") as f:
        f.write(content)

    print(f"✅ Owner page generated: {filename}")
