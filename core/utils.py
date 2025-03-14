import requests
from requests import Session

API_KEY = "4016eec07bf11e741a1c0024"
BASE_URL = "https://v6.exchangerate-api.com/v6/"

class ExchangeRate:
    def __init__(self):
        self.base_url = f'{BASE_URL}{API_KEY}'
        # self.api_key = api_key
        self.session = Session()

    def get_price(self, present, new):
        url = f"{self.base_url}/pair/{present}/{new}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "API request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# exchange = ExchangeRate()
# result = exchange.get_price("USD", "NGN")
# rate = result['conversion_rate']
# print(rate)