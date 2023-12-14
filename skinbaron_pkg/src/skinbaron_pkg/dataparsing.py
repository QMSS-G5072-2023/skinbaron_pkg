import pandas as pd

class DataProcessor:
    """
    class for parsing JSON data obtained from skinbaron api to DataFrame.
    """
    @staticmethod
    def json_to_dataframe(json):
        """
        Converts JSON object into DataFrame.
        :param json (dict): The JSON object needs to be converted.
        :return DataFrame: DataFrame converted from the JSON input.
        :raises Exception: If the JSON data cannot converted into DataFrame.
        """
        # try:
        #     return pd.json_normalize(json_data, record_path=['data'])
        # except Exception as e:
        #     print(f"Error in processing JSON data: {e} for {json_data}")

        json_data = {
            "data": json.get(list(json.keys())[0])
        }

        try:
            new_df = pd.json_normalize(json_data, record_path=['data'])
            return new_df
        except Exception as e:
            print(f"Error in processing JSON data: {e} for {json}")

# Example Usage
if __name__ == "__main__":
    from skinbaron_api import SkinBaronAPI
    api_key = "api_key_here"
    app_id = "skinbaron_account_app_id"
    api = SkinBaronAPI(api_key, app_id)
    bestdeals = api.best_deals(size=100)
    bestdeals_df = DataProcessor.json_to_dataframe(bestdeals)
    print(bestdeals_df)