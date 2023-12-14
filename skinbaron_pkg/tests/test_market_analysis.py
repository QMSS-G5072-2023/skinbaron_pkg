import pytest
import pandas as pd
import numpy as np
from skinbaron_pkg.src.market_analysis import ItemFilter
from skinbaron_pkg.src.skinbaron_api import SkinBaronAPI
from skinbaron_pkg.src.dataparsing import DataProcessor as dp
api_key = " "
app_id = " "
api = SkinBaronAPI(api_key, app_id)
newitems = api.newest_items(size=100)
bestdeals = api.best_deals(size=100)
newitems_df = dp.json_to_dataframe(newitems)
bestdeals_df = dp.json_to_dataframe(bestdeals)

def test_filter_items_no_params():
    item_filter = ItemFilter(newitems_df, bestdeals_df)
    filtered_df = item_filter.filter_items()
    assert not filtered_df.empty
    assert len(filtered_df) == len(newitems_df) + len(bestdeals_df)

def test_filter_items_by_name():
    item_filter = ItemFilter(newitems_df, bestdeals_df)
    filtered_df = item_filter.filter_items(itemName= 'SG 553 | Bleached')
    assert all(filtered_df['itemName'] == 'SG 553 | Bleached')

def test_filter_items_by_rarity_and_exterior():
    item_filter = ItemFilter(newitems_df, bestdeals_df)
    filtered_df = item_filter.filter_items(rarityName='Consumer Grade', exteriorName='Factory New')
    assert not filtered_df.empty
    assert all(filtered_df['rarityName'] == 'Consumer Grade')
    assert all(filtered_df['exteriorName'] == 'Factory New')


