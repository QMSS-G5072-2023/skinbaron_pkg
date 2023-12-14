import pytest
import numpy as np
from skinbaron_pkg.src.visualization_prediction import MarketTrends, PricePrediction
import pandas as pd
from datetime import datetime

mock_data = {
    'dateSold': [['2023-01-01', '2023-01-02'], ['2023-01-01', '2023-01-03']],
    'price': [[100, 110], [150, 160]],
    'lowestPrice': [105, 155],
    'itemName': ['Item1', 'Item2'],
    'exteriorName': ['Condition1', 'Condition2'],
    'dopplerPhase': ['Phase1', 'Phase2'],
    'statTrak': [False, False],
    'souvenir': [False, False],
    'quantity' : [1, 3],
    'url': ['Nicole', 'Guo'],
    'label': ['so', 'sleepy']

}
newestsales_df = pd.DataFrame(mock_data)

def test_price_trend():
    processed_df = MarketTrends.price_trend(newestsales_df)
    assert 'dateSold' in processed_df.columns
    assert 'price' in processed_df.columns
    assert len(processed_df['price'].iloc[0]) == 3 # very important!!!
    # if the lowest price correctly updated into the into price column!!!

def test_price_prediction():
    processed_df = MarketTrends.price_trend(newestsales_df)
    prediction_df = PricePrediction.price_prediction(processed_df)
    assert 'predicted_price_7_days' in prediction_df.columns
    # print("!!!!!!!!!!!!", type(processed_df['predicted_price_7_days'].iloc[0]))
    assert isinstance(processed_df['predicted_price_7_days'].iloc[0], np.float64)

