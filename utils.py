import pandas as pd
import gspread
import streamlit as st
from google.oauth2 import service_account

@st.cache_data(ttl=600)
def load_data():
    creds_dict = {
      "type": "service_account",
      "project_id": "internship-project-461810",
      "private_key_id": "2a026d032cfb5943f730167912d967ef21fca748",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6o3PZQqXGbxQQ\nKFeYGcxMpPmxWYPoEXNCUuUGvOOtiFAg9KeV2k/rzoDIxJDpIxibDHrHvZ8X5NXj\nPpii5zJ5fGAlp2NSv8EmBR6SqKhHWk/IvQSzuZDpq6Mnlu4feLMUxh+1Cpm09IWV\nge79Ft7PESk6Vjt3sZKS6A7QacO05B44o+Lixn6Fm3r7AcPwqSfDA4l7uk8N9zl8\n5GkdUI+DbkdTFhGDLh7esPvYQkD17eOpBaNPsC/f8BJr1o6j4gZeec1OhJPFI+wB\n1FBz/QpSdB+Pg4y9diKKilwxcFxKF3gbRaV9Vipkff5215uzQ1z1JK7aF1TBCPjM\nJasHUjK3AgMBAAECggEADJMZqZAneiSeve3x5OIMFTfiSNQmonqWgOfz3U3ZqyXt\nfCLvrZV9X/5UR/KSbtq5/CxNk2qPrvzwejSL9SHNkUjTc4YBF6Cqw0SCCFCLse8A\nRB6UFAXTISM6xV6SYZVwv1wP49M4guwcmfOcpfml/l6CIBeSPyC8JuCyqtENagD9\nIe8+4L5UFRkfH9VhHwVvJId7KOlc7Ztc6RsdCDGEAQCQzjH3Lhq18T8+KFebDGjF\nUYO8g9rnDL82hXUKjKSPvwXSBJiYFZVl3swmBQmC+GFlceGVV2FOCgXX/0r6n0nI\nrq4QfFZSYO4wM5z/TdwTLDw1VpKbKiqUggcKi/fVMQKBgQDaufZrTWTtKyBErXzL\nzMn/5b9dagHfXSq0sFKJ5LTLvLA3DJJqNmjmahmN6aq6zq4Ua1WBv3epSveclQ/j\njPc721MA9MNE9ujU/H7TBIFHnk4IMXS5wqrL3/rffHWmy7e44qJnASi03XO1FlT4\nkL0tSOd29LuwDLAN7ml77O+T8QKBgQDacaPESdp2DN3Rr3F90C2IKs3boa1uCj3O\nUQSo2W98yCE+0Pperc1dGYbpTajsdDIr7joABJ2WDaK5k250fjKhuF8BUWZcCwzi\nbIEDRBXdUlkt/dessAYTEwr6bGSNTLi+hxEo870OmkjservO1EpZ+nyc0Y/Woukv\nPpVzXwI5JwKBgEmGJW1gcMLAsnIjl0Wyq1xX0IIINmTtHoPqmXQ86wFphhqbIUSO\n0ahSlhB8MaXl/+JhSjb5M7I2vxFlkhe9tQXr7fTuUg2GqjGeRsuMQiDe+AAND925\nsEwkGGKzpaDR7go6NLlHTHWv00tWHG4JyW3FifkUv1qoiS3FrLO5q7chAoGASfxV\nYGU3NeaTtrJ6eQdqdIUy5iGzcOLNHjT4pAvJI/VQtUrokerB9Ldxp1FjVnrgh1qP\nkHP/v9PsenhB3/jiQz4EB5k/VwtzGLlxVN7ZnPWIOPiR9O5FkG5RuJG/2M/UfsuW\nd01eijSdYGMNezcR27noPOEJm8PfwN2slr/mK98CgYEAtGZN/ovE2pdpYK8YGRxQ\n7BV49EXyWmMweQmLCiwTXK9Fd3agqdObltF7tKqy4B5KbPGdolZYPOOW7E6KojlL\nUcOLfSmhQv6rBTeWdBFUXPDCJgZxcqmXmT7EkxCv/whKQF/uBZ4pmXt1P8nO2l//\nXXQEOQWZ6fmF6AztR/z2TGo=\n-----END PRIVATE KEY-----\n",
      "client_email": "sheet-accessor@internship-project-461810.iam.gserviceaccount.com",
      "token_uri": "https://oauth2.googleapis.com/token"
    }

    creds = service_account.Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)

    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1sjfGn--p6WGLPpsE5TdvNSHiuoFyy7IT6ACwlsRgwgg/edit?usp=sharing")
    data = sheet.worksheet("Cleaned_April").get_all_records()
    df_apr = pd.DataFrame(data)
    
    data_march = sheet.worksheet("Cleaned_March").get_all_records()
    df_mar = pd.DataFrame(data_march)
    
    df_all = pd.concat([df_apr, df_mar], ignore_index=True)
    return df_all
