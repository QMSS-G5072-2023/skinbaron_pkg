import pytest
from skinbaron_pkg.src.skinbaron_api import SkinBaronAPI

api_key = " "
app_id = " "
api = SkinBaronAPI(api_key, app_id)

def test_get_price_list():
    response = api.get_price_list()
    assert isinstance(response, dict)
    assert 'map' in response

def test_newest_items():
    size = 10
    response = api.newest_items(size)
    assert isinstance(response, dict)
    assert 'newestItems' in response

def test_best_deals():
    size = 10
    response = api.best_deals(size)
    assert isinstance(response, dict)
    assert 'bestDeals' in response

def test_newest_sales_30_days():
    item_name = "AK-47 | Redline"
    stat_trak = False
    souvenir = False
    response = api.newest_sales_30_days(item_name, stat_trak, souvenir)
    assert isinstance(response, dict)
    assert 'newestSales30Days' in response
