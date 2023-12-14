import pytest
import pandas as pd
import numpy as np
from skinbaron_pkg.src.market_analysis import ItemFilter
from skinbaron_pkg.src.skinbaron_api import SkinBaronAPI as skb
from skinbaron_pkg.src.dataparsing import DataProcessor as dp
from skinbaron_pkg.src.data_utils import Report_generator as rg
token = " "
appID = " "
report_generator = rg(token, appID)



def test_separate_item_and_condition():
    test_cases = [
        ('★ Butterfly Knife | Gamma Doppler (Factory New)', ('★ Butterfly Knife | Gamma Doppler', 'Factory New')),
        ('P90 | Freight (Well-Worn)', ('P90 | Freight', 'Well-Worn')),
        ('Item Without Condition', ('Item Without Condition', None))
    ]
    for input_str, expected_output in test_cases:
        assert report_generator.separate_item_and_condition(input_str) == expected_output


def test_cheapest():
    pricelist_df_data = {'itemName': ['Item1'], 'exteriorName': ['Condition1'], 'dopplerPhase': ['Phase1'],
                         'lowestPrice': [100], 'quantity': [5], 'url': ['qingxuanhaha']}
    df_data = {'itemName': ['Item1'], 'exteriorName': ['Condition1'], 'dopplerPhase': ['Phase1'], 'price': [[100, 200]],
               'dateSold': [['2020-01-01', '2020-02-01']]}

    pricelist_df = pd.DataFrame(pricelist_df_data)
    df = pd.DataFrame(df_data)

    merged_df = report_generator.cheapest(pricelist_df, df)
    assert not merged_df.empty
    assert 'itemName' in merged_df.columns
    assert 'exteriorName' in merged_df.columns
    assert merged_df.shape[0] == 1
    assert merged_df.shape[1] == 8


def test_newestsales_df_pipeline():
    merged_df = report_generator.newestsales_df_pipeline(skb, dp.json_to_dataframe, report_generator.cheapest,
                                                         report_generator.separate_item_and_condition, token, appID,
                                                         '★ Butterfly Knife | Gamma Doppler', False,
                                                         False)
    assert merged_df.shape[0] == 4
    assert all(merged_df['itemName'] == '★ Butterfly Knife | Gamma Doppler')
    assert all(merged_df['statTrak'] == False)
