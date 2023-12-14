from skinbaron_api import SkinBaronAPI as skb
from dataparsing import DataProcessor as dp
from market_analysis import ItemFilter
from data_utils import Report_generator as rg
from visualization_prediction import MarketTrends, PricePrediction

# example usage of all the python files
if __name__ == '__main__':

    token = 'api_key_here'
    appID = 'skinbaron_account_app_id'
    api = skb(api_key = token, app_id = appID)
    pricelist = api.get_price_list()
    print(f"pricelist: {pricelist}")
    print('====================================')
    newitems = api.newest_items(size=100)
    bestdeals = api.best_deals(size=100)


    # Convert API data to DataFrame
    pricelist_df = dp.json_to_dataframe(pricelist)
    newitems_df = dp.json_to_dataframe(newitems)
    bestdeals_df = dp.json_to_dataframe(bestdeals)
    print(f"newitems_df: {newitems_df}")
    print('====================================')

    # ItemFilter
    item_filter = ItemFilter(newitems_df, bestdeals_df)
    filtered_items = item_filter.filter_items()
    print(f"filtered_items: {filtered_items}")
    print('====================================')
    report_generator = rg(api_key = token, app_id = appID)
    merged_df = report_generator.newestsales_df_pipeline(skb, dp.json_to_dataframe, report_generator.cheapest,
                                        report_generator.separate_item_and_condition, token,appID, '★ Butterfly Knife | Gamma Doppler', False,
                                        False)
    print(f'merged_df:{merged_df}')
    print('====================================')

    market_price_trend = MarketTrends.price_trend(merged_df)
    print(f'market_price_trend:{market_price_trend}')
    print('====================================')
    market_price_prediction = PricePrediction.price_prediction(market_price_trend)
    print(f'price_prediction:{market_price_prediction}')
    print('====================================')

    # # Perform market trend analysis
    # trend_data = MarketTrends.price_trend(filtered_items)
    # print(trend_data)
    # print('====================================')
    #
    # # Predict future prices
    # predicted_prices = PricePrediction.price_prediction(trend_data)
    # print(predicted_prices)
    # print('====================================')

    # Example usage of newestsales_df_pipeline
    # merged_df = newestsales_df_pipeline(skb.GetNewestSales30Days, skb.GetPriceList, skb.dataframe_pipeline, cheapest,
    #                                     separate_item_and_condition, token, '★ Butterfly Knife | Gamma Doppler', False,
    #                                     False)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
