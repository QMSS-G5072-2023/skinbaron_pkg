import requests

class SkinBaronAPI:

    """
    A class to interact with the SkinBaron API.
    provides methods to fetch different data from the SkinBaron API, such as price lists, newest items, best deals, and sales data over the last 30 days.

    Attributes:
        BASE_URL (str): base URL for the SkinBaron API.
        HEADERS (dict): Default headers for API requests.
        api_key (str): API key for the SkinBaron API.
        app_id (str): Application ID for the SkinBaron account.(Note: each account has its identical app_id)
    """

    BASE_URL = "https://api.skinbaron.de"
    HEADERS = {
        'Content-Type': 'application/json',
        'x-requested-with': 'XMLHttpRequest'
    }

    def __init__(self, api_key, app_id):
        """
        Initializes the SkinBaronAPI class
        :param api_key: API key for the SkinBaron API.
        :param app_id: Application ID for the SkinBaron account.
        """
        self.api_key = api_key
        self.app_id = app_id

    def _post_request(self, endpoint, data):
        """
        Sends a POST request to a specified endpoint of the SkinBaron API.
        :param endpoint (str): The API endpoint to which the request is sent.
        :param data (dict): Data to be sent in the request.
        :return (dict): JSON response from the API.
        :raises Exception: If the post request failed.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        data.update({"apikey": self.api_key, "appId": self.app_id})
        try:
            response = requests.post(url, json=data, headers=self.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_price_list(self):
        """
        Fetches the price list from the SkinBaron API.
        :return (dict): JSON response of the price list data.
        """
        return self._post_request("GetPriceList", {})

    def newest_items(self, size):
        """
        Fetches the list of newest items based on the specified size.
        :param size (int): The number of newest items to retrieve. limit: max 100
        :return (dict): JSON response of the newest listed items.
        """
        return self._post_request("NewestItems", {"size": size})

    def best_deals(self, size):
        """
        Fetches the list of best deals based on the specified size.
        :param size (int): The number of best deals to retrieve. limit: max 100
        :return (dict): JSON response of the best deals listed on market.
        """
        return self._post_request("BestDeals", {"size": size})

    def newest_sales_30_days(self, item_name, stat_trak, souvenir, doppler_phase=None):
        """
        Fetches the sales data for the last 30 days for a specific item.
        :param item_name (str): Name of the item. (this do not have to be precise)
        :param stat_trak (bool): whether the item is StatTrak.
        :param souvenir (bool): whether the item is a souvenir.
        :param doppler_phase (str, optional): The doppler phase of the item.
        :return dict: JSON response of the historical trading data for the last 30 days.
        """
        data = {
            "itemName": item_name,
            "statTrak": stat_trak,
            "souvenir": souvenir
        }
        if doppler_phase:
            data["dopplerPhase"] = doppler_phase
        return self._post_request("GetNewestSales30Days", data)


# Example Usage
if __name__ == "__main__":
    api_key = "api_key_here"
    app_id = "skinbaron_account_app_id"
    api = SkinBaronAPI(api_key, app_id)

    price_list = api.get_price_list()
    newest_items = api.newest_items(50)
    best_deals = api.best_deals(50)
    newest_sales = api.newest_sales_30_days("AK-47 | Redline", False, False)

    print(price_list)
    print(newest_items)
    print(best_deals)
    print(newest_sales)