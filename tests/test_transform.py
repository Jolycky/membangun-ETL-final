import pytest
import pandas as pd
from utils.transform import transform_data

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Title": ["Product A", "Unknown Product", "Product B"],
        "Price": ["$10", "Price Unavailable", "$15"],
        "Rating": ["Rating: 4.5", "Rating: 5.0", None],
        "Colors": ["Colors (2)", "Colors (3)", "Colors (4)"],
        "Size": ["Size: M", "Size: L", "Size: S"],
        "Gender": ["Gender: Unisex", "Gender: Male", "Gender: Female"],
        "timestamp": ["2024-01-01T00:00:00"] * 3
    })

def test_transform_data(sample_data):
    transformed = transform_data(sample_data)
    assert isinstance(transformed, pd.DataFrame)
    assert "Unknown Product" not in transformed["Title"].values
    assert transformed["Price"].dtype == float
    assert all(transformed["Price"] >= 0)
    assert transformed["Rating"].dtype == float
    assert transformed["Colors"].dtype == int
    assert not transformed.isnull().values.any(), "Data should not contain NaN"