import pandas as pd
import gspread
from google.oauth2 import service_account
from sqlalchemy import create_engine


# Menyimpan data dalam format .csv
def save_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print("File CSV berhasil disimpan.")
    except Exception as e:
        print(f"Gagal menyimpan file CSV: {e}")

# Menyimpan data ke google sheets
def save_to_google_sheets(df, spreadsheet_name="fashion studio", worksheet_name="Sheet1", creds_path="my-project.json"):
    try:
        import gspread
        from gspread_dataframe import set_with_dataframe
        from google.oauth2.service_account import Credentials

        # Scope akses Google Sheets
        scope = ["https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive"]


        # Autentikasi dengan credentials JSON
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)

        # Buka spreadsheet
        spreadsheet = client.open(spreadsheet_name)

        # Pilih worksheet (atau buat baru kalau belum ada)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

        worksheet.clear()  # Kosongkan sheet sebelum menulis ulang
        set_with_dataframe(worksheet, df)
        print("Data berhasil disimpan ke Google Sheets.")

    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")

# Menyimpan data ke PostgreSQL
def save_to_postgresql(df, db_url="postgresql://postgres:1234@localhost:5432/fashion_studio", table_name="products"):
    try:
        from sqlalchemy import create_engine

        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")

