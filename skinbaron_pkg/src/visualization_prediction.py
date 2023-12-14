
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from skinbaron_api import SkinBaronAPI
from dataparsing import DataProcessor



class MarketTrends:
    """
    A class to analyze market trends of items based on their price history.
    visualize the price trends of different user selected items over time using a line plot.
    """
    @staticmethod
    def price_trend(newestsales_df):
        """
            Processes sales data to show price trends and generates a line plot for visualization.
            This function combinds sales data with the current market price and the lowest price,
            and then visualizes the price trends using a line plot.

            :param newestsales_df (DataFrame): DataFrame containing the sales data.
            :return: A DataFrame with updated sales data and visualized price trends.

            The function includes internal helper functions to parse date and price lists from strings
            and generates a line plot to show the price trends over time for each item.

            Example:
            ```
            df = Report_generator.newestsales_df_pipeline(endpointname, currentprice_endpoint, general_pipeline, reportgenerator, regex_item,
            api_key, itemName, statTrak, souvenir, dopplerPhase = None)
            price_trend_df = price_trend(df)
            print(price_trend_df)
            ```
            """
        data_new_cleaned = newestsales_df.dropna(subset=['dateSold', 'price'])
        today_date = datetime.now().strftime('%Y-%m-%d')

        data_new_cleaned['dates'] = [data_new_cleaned['dateSold'][i].append(today_date) for i in
                                     range(data_new_cleaned.shape[0])]
        data_new_cleaned['prices'] = [data_new_cleaned['price'][i].append(data_new_cleaned['lowestPrice'][i]) for i in
                                      range(data_new_cleaned.shape[0])]
        data_new_cleaned = data_new_cleaned[
            data_new_cleaned.apply(lambda x: len(x['price']) == len(x['dateSold']), axis=1)]

        def parse_date_list(date_str):
            date_str = date_str.strip('[]')
            date_list = date_str.split(', ')
            return [pd.to_datetime(date.strip("'")) for date in date_list]

        def parse_price_list(price_str):
            price_str = price_str.strip('[]')
            price_list = price_str.split(', ')
            return [float(price) for price in price_list]

        updated_dates = []
        updated_prices = []
        updated_labels = []

        for index, row in data_new_cleaned.iterrows():
            label = f"{row['itemName']} | {row['exteriorName']} {row['dopplerPhase']}"

            if isinstance(row['dateSold'], str):
                x_values = parse_date_list(row['dateSold'])
                y_values = parse_price_list(row['price'])
            else:
                x_values = [pd.to_datetime(date) for date in row['dateSold']]
                y_values = [float(price) for price in row['price']]

            # Sort the data based on dates for chronological order
            combined = sorted(zip(x_values, y_values))
            x_values_sorted, y_values_sorted = zip(*combined)

            updated_dates.append(list(x_values_sorted))
            updated_prices.append(list(y_values_sorted))
            updated_labels.append(label)

        data_new_cleaned['dateSold'] = updated_dates
        data_new_cleaned['price'] = updated_prices
        data_new_cleaned['label'] = updated_labels

        data_new_cleaned = data_new_cleaned.drop(columns=['dates', 'prices'])

        # generate plot
        df = data_new_cleaned.copy()
        fig, ax = plt.subplots(figsize=(10, 6))

        for index, row in df.iterrows():
            label = f"{row['label']}"
            x_values_sorted = row['dateSold']
            y_values_sorted = row['price']

            ax.plot(x_values_sorted, y_values_sorted, label=label)

        ax.set_title('Item Price Trends Over Time')
        ax.set_xlabel('Date Sold')
        ax.set_ylabel('Price')
        ax.legend()
        plt.show()

        return data_new_cleaned

class PricePrediction:
    """
    predict future prices of items based on historical price trends.
    """
    @staticmethod
    def price_prediction(price_trend_df):
        """
        Predicts future prices of items based on historical price trends.

        This function uses LR to predict the price of each item 7 days after the current date,
        based on the price trend data provided. The prediction is 7 days is because it considers CSGO market restrictions
        on selling newly purchased products only after 7 days.

        :param price_trend_df (DataFrame): DataFrame containing price trend data.
        :return: A DataFrame with predicted prices 7 days into the future and other relevant item details.

        The function includes internal helper functions to parse date and price lists from strings.

        Example:
        ```
        df = Report_generator.newestsales_df_pipeline(endpointname, currentprice_endpoint, general_pipeline, reportgenerator, regex_item,
        api_key, itemName, statTrak, souvenir, dopplerPhase = None)
        price_prediction_df = MarketTrends.price_prediction(price_trend(df))
        print(price_prediction_df)
        ```
        """
        data = price_trend_df

        def custom_parse_dates(date_str):
            if isinstance(date_str, str):
                date_list = date_str.strip('[]').split(', ')
                return [pd.to_datetime(date.strip("'")) for date in date_list]
            else:
                return [pd.to_datetime(date) for date in date_str]

        def custom_parse_prices(price_str):
            if isinstance(price_str, str):
                price_list = price_str.strip('[]').split(', ')
                return [float(price) for price in price_list]
            else:
                return price_str

        today = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        prediction_date = today + timedelta(days=7)

        predictions = []
        for index, row in data.iterrows():
            dates = custom_parse_dates(row['dateSold'])
            prices = custom_parse_prices(row['price'])

            days_since_start = np.array([(date - dates[0]).days for date in dates]).reshape(-1, 1)

            model = LinearRegression()
            model.fit(days_since_start, prices)

            # Predict price 7 days after today
            prediction_day = (prediction_date - dates[0]).days
            predicted_price = model.predict([[prediction_day]])[0]
            predictions.append(predicted_price)

        data['predicted_price_7_days'] = predictions
        data = data[['predicted_price_7_days', 'itemName', 'exteriorName', 'dopplerPhase', 'price', 'dateSold',
                     'statTrak', 'souvenir', 'lowestPrice', 'quantity', 'url', 'label']]
        return data