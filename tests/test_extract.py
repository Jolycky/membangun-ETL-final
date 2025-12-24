import pytest
from utils.extract import scrape_main
import pandas as pd

def test_scrape_main_basic():
    df = scrape_main(max_pages=1)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "Scraped DataFrame should not be empty"
    required_columns = {"Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"}
    assert required_columns.issubset(df.columns), "Missing expected columns"