from unittest.mock import patch, MagicMock, mock_open
import pytest
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql
from google.oauth2.service_account import Credentials
import os

@pytest.fixture
def dummy_df():
    return pd.DataFrame({
        "Title": ["Product A"],
        "Price": [160000.0],
        "Rating": [4.5],
        "Colors": [2],
        "Size": ["M"],
        "Gender": ["Unisex"],
        "timestamp": ["2024-01-01T00:00:00"]
    })

def test_save_to_csv(tmp_path, dummy_df):
    filepath = tmp_path / "test_output.csv"
    save_to_csv(dummy_df, filename=str(filepath))
    assert os.path.exists(filepath)

@patch("utils.load.service_account.Credentials.from_service_account_file")
@patch("utils.load.gspread")
@patch("utils.load.gspread.authorize")
def test_save_to_google_sheets(mock_from_service_account_file, mock_gspread, mock_authorize, dummy_df):
    # Mock autentikasi dan client Google Sheets
    mock_creds = MagicMock()
    mock_from_service_account_file.return_value = mock_creds
    mock_creds.with_scopes.return_value = mock_creds

    mock_client = MagicMock()
    mock_sheet = MagicMock()

    # Simulasikan worksheet tidak ditemukan (tambah worksheet baru)
    class WorksheetNotFound(Exception):
        pass
    mock_gspread.exceptions.WorksheetNotFound = WorksheetNotFound
    mock_authorize.return_value = mock_client
    mock_client.open.return_value.worksheet.side_effect = WorksheetNotFound()
    mock_client.open.return_value.add_worksheet.return_value = mock_sheet

    # Jalankan fungsi
    save_to_google_sheets(dummy_df, creds_path="fake-creds.json")

    # Verifikasi authorize dipanggil
    mock_authorize.assert_called_once()

@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_create_engine, dummy_df):
    # Mock engine PostgreSQL
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    save_to_postgresql(dummy_df)
    mock_engine.dispose.assert_not_called()