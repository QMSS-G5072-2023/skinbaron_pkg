# data_utils.py
import pandas as pd
import re
class Report_generator:
    """
    A class for generating reports and processing item data.

    separating item names and conditions, generating detailed reports based on item's historical and current market prices,
    and a data pipeline for data processing.

    Attributes:
        api_key (str): API key for API.
        app_id (str): Application ID for the SkinBaron account. (Note: each account has its identical app_id)
    """
    def __init__(self, api_key, app_id):
        self.api_key = api_key
        self.app_id = app_id
    def separate_item_and_condition(self, s):

        """
        Separates the item name and its condition from a combined string.

        This function uses regex to split a string into the item name and its condition (e.g., 'Factory New').
        This is a helper function for newestsales_df_pipeline

        :param s (str): The combined string of item name and condition.
        :return: A tuple containing the item name and its condition.

        Example:
        ```
        item1 = '★ Butterfly Knife | Gamma Doppler (Factory New)'
        item2 = 'P90 | Freight (Well-Worn)'
        item1_name, item1_condition = separate_item_and_condition(item1)
        item2_name, item2_condition = separate_item_and_condition(item2)
        print(f"'{item1}' becomes '{item1_name}' and '{item1_condition}'")
        print(f"'{item2}' becomes '{item2_name}' and '{item2_condition}'")
        its printed output would be:
        '★ Butterfly Knife | Gamma Doppler (Factory New)' becomes '★ Butterfly Knife | Gamma Doppler' and 'Factory New'
        'P90 | Freight (Well-Worn)' becomes 'P90 | Freight' and 'Well-Worn'
        ```
        """

        match = re.match(r"(.*) \(([^)]+)\)$", s)
        if match:
            item_name = match.group(1).strip()
            condition = match.group(2).strip()
            return item_name, condition
        else:
            return s, None

    def cheapest(self, pricelist_df, df):

        """
        Further cleans the data
        Generates a report based on the item's historical and current market price.

        This function merges historical sales data with current market listings to provide a comprehensive report.
        includes details like item name, condition, doppler phase, historical trading info, and current market listings.
        This is a helper function for newestsales_df_pipeline

        :param pricelist_df (DataFrame): DataFrame containing current market listing prices.
        :param df (DataFrame): DataFrame containing historical sales data.
        :return: A merged DataFrame with both historical and current market data.

        Example:
        ```
        df = cheapest(pricelist_df, df)
        print(df)
        ```
        """

        grouped_df = df.groupby(['itemName', 'exteriorName', 'dopplerPhase']).agg({'price': list, 'dateSold': list})
        grouped_df = grouped_df.reset_index()
        pricelist_df = pricelist_df.rename(columns={'dopplerClassName': 'dopplerPhase'})
        merged_df = pd.merge(grouped_df, pricelist_df, on=['itemName', 'exteriorName', 'dopplerPhase'], how='left')
        lengths_of_price_lists = [len(merged_df['price'].iloc[i]) for i in range(merged_df.shape[0])]
        most_trade = max(lengths_of_price_lists)

        print(f"Report based on your search:\n"
              f"There are a total of {merged_df.shape[0]} items matches your search")

        for i in range(merged_df.shape[0]):
            print(f"======================================================================\n"
                  f"The {i+1}th item is {merged_df['itemName'].iloc[i]}, its condition is {merged_df['exteriorName'].iloc[i]}, its dopplerphase is {merged_df['dopplerPhase'].iloc[i]}\n"
                  f"Historical trading info: during the past 30 days, it's been trade for {len(merged_df['price'].iloc[i])} times on {merged_df['dateSold'].iloc[i]} with price of {merged_df['price'].iloc[i]}\n"
                  f"Current market info: There are currently {merged_df['quantity'].iloc[i]} of them are listed for sale, the lowest price would be {merged_df['lowestPrice'].iloc[i]}, you could access through this link: {merged_df['url'].iloc[i]}")
            if len(merged_df['price'].iloc[i]) == most_trade:
                print(f"Note: This is the most frequent traded item during the past 30 days!!")
        print("=======================end of the report=======================")

        return merged_df

    def newestsales_df_pipeline(self, skb, general_pipeline, reportgenerator, regex_item, api_key,appID, itemName, statTrak, souvenir, dopplerPhase = None):
        """
        Processes and merges data from different endpoints to provide structured sales data.

        This function fetches data from two specified endpoints by calling GetNewestSales30Days and GetPriceList,
         structures data with the two helper functions above and more, and merges it to create a detailed report.
         It supports both precise and vague item searches.

        :param endpointname: Function to fetch newest sales data.
        :param currentprice_endpoint: Function to fetch current price listings.
        :param general_pipeline: Function to process and structure the data.
        :param reportgenerator: Function to generate a detailed report.
        :param regex_item: Function to extract item details using regex.
        :param api_key (str): API key for authentication.
        :param itemName (str): Name of the item to search.
        :param statTrak (bool): Whether to filter by StatTrak.
        :param souvenir (bool): Whether to filter by souvenir.
        :param dopplerPhase (str, optional): Specific doppler phase to filter.
        :return: A structured DataFrame with detailed sales and market data.

        Example:
        ```
        1. example of search item with specific requirements
        merged_df = newestsales_df_pipeline(GetNewestSales30Days,GetPriceList, dataframe_pipeline,cheapest,
        separate_item_and_condition, token, '★ Butterfly Knife | Gamma Doppler', False, False)
        print(merged_df)

        2. if buyers want to use vague search
        (please note, due to search capability, even with vague search, this function requires to enter at least 3 characters
        for the param itemName)
        merged_df = newestsales_df_pipeline(GetNewestSales30Days,GetPriceList, dataframe_pipeline,cheapest,
        separate_item_and_condition, token, 'Knife', False, False)
        print(merged_df)

        ```
        """
        api = skb(api_key=api_key, app_id=appID)
        pricelist = api.get_price_list()

        pricelist_df = general_pipeline(pricelist)
        results = pricelist_df['marketHashName'].apply(lambda x: regex_item(x))
        pricelist_df['itemName'] = results.apply(lambda x: x[0])
        pricelist_df['exteriorName'] = results.apply(lambda x: x[1])
        pricelist_df = pricelist_df[['itemName', 'exteriorName', 'statTrak', 'souvenir', 'lowestPrice','quantity','url', 'dopplerClassName']]
        # pricelist_df = 1

        df = api.newest_sales_30_days(itemName, statTrak, souvenir, dopplerPhase)
        df = general_pipeline(df)
        results = df['itemName'].apply(lambda x: regex_item(x))
        df['itemName'] = results.apply(lambda x: x[0])
        df['exteriorName'] = results.apply(lambda x: x[1])
        merged_df = reportgenerator(pricelist_df, df)
        return merged_df