import pytest
import pandas as pd
from skinbaron_pkg.src.dataparsing import DataProcessor

def test_json_to_dataframe_valid():
    json_input = {
        "items": [
            {"id": 1, "name": "Item 1", "price": 10},
            {"id": 2, "name": "Item 2", "price": 20}
        ]
    }

    cols = ['id', 'name', 'price']
    result_df = DataProcessor.json_to_dataframe(json_input)

    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == cols
    assert len(result_df) == 2

def test_json_to_dataframe_empty():
    json_input = {"items": []}
    result_df = DataProcessor.json_to_dataframe(json_input)

    assert isinstance(result_df, pd.DataFrame)
    assert result_df.empty

def test_json_to_dataframe_invalid():
    json_input = "invalid"

    with pytest.raises(Exception):
        _ = DataProcessor.json_to_dataframe(json_input)

