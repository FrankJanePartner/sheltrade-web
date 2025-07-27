"""
Utility class for interacting with the CoinGecko API to fetch cryptocurrency prices.
"""

import requests
from requests import Session, Timeout

BASE_URL = "https://api.coingecko.com/api/v3/simple/"

class COINGECKOAPI:
    """
    A class to interact with the CoinGecko API for fetching cryptocurrency prices.

    Methods:
        getprice(coin, currency): Fetches the current price of a cryptocurrency in a specified currency.
    """

    def __init__(self):
        """
        Initializes the COINGECKOAPI class with a session and headers.
        """
        self.base_url = BASE_URL
        self.headers = {"accept": "application/json"}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getprice(self, coin, currency):
        """
        Fetches the current price of a cryptocurrency in a specified currency.

        Args:
            coin (str): The cryptocurrency ID (e.g., 'ethereum').
            currency (str): The target currency (e.g., 'usd').

        Returns:
            dict: JSON response containing the price or error information.
        """
        url = f"{self.base_url}price?ids={coin}&vs_currencies={currency}"
        try:
            response = self.session.get(url, timeout=10)  # Increased timeout
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "API request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Example usage:
# coingecko = COINGECKOAPI()
# c = coingecko.getprice('ethereum', 'usd')
# print(c)  # {'ethereum': {'usd': 2802.57}}
