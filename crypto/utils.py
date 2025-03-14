import requests
from requests import Session, Timeout

BASE_URL = "https://api.coingecko.com/api/v3/simple/"

class COINGECKOAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"accept": "application/json"}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getprice(self, coin, currency):
        url = f"{self.base_url}price?ids={coin}&vs_currencies={currency}"
        try:
            response = self.session.get(url, timeout=10)  # Increased timeout
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "API request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Create an instance before calling the method
# coingecko = COINGECKOAPI()
# c = coingecko.getprice('ethereum', 'usd')
# print(c)

# {'ethereum': {'usd': 2802.57}}