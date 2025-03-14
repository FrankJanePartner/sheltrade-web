import requests
from bs4 import BeautifulSoup


class VTUAPI:
    def __init__(self, api_key, public_key, secret_key):
    
        self.base_url = BASE_URL
        self.headers = {
            "Accept": "application/json",
            "api-key": api_key,
            "Public-Key": public_key,
            "Secret-key": secret_key,
        }
        self.session = Session()
        self.session.headers.update(self.headers)

# Function to get market value of a gift card
    def get_gift_card_value(card_name):
        url = f"https://www.examplemarketplace.com/search?q={card_name}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Failed to fetch data: {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Adjust selectors based on the site’s HTML structure
        price = soup.find('span', class_='card-price')
        if price:
            return price.text.strip()
        return "Price not found"

    # Function to check if a gift card is valid
    def check_gift_card_validity(card_number, pin):
        url = "https://http://www.cardbalance.net//check-balance"
        data = {
            "card_number": card_number,
            "pin": pin
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            return f"Failed to check balance: {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')
        balance = soup.find('span', class_='card-balance')
        if balance:
            return balance.text.strip()
        return "Invalid card or balance not found"

# Example usage
if __name__ == "__main__":
    card_name = "Amazon Gift Card"
    market_value = get_gift_card_value(card_name)
    print(f"Market Value of {card_name}: {market_value}")

    card_number = "1234567890"
    pin = "1234"
    validity = check_gift_card_validity(card_number, pin)
    print(f"Card Validity/Balance: {validity}")


# import requests
# from bs4 import BeautifulSoup
# from decouple import config
# import json
# import requests
# from requests import Session
# import random
# import string
# from datetime import datetime
# import pytz

# API_KEY = "801ea9e2f2d9234d3437de7074ad4af6"
# PUBLIC_KEY = "PK_3921bc1b243a21a3a8b490b75f0932bf0f1aaf349bb"
# SECRET_KEY = "SK_501457b076cb4065af6c13f236d716fca33aa432967"
# BASE_URL = "https://www.giftkarte.com/vendor/api/validate"
# optional link = https://www.giftkarte.com/voucher_authentication
# "success" => true
# "challenge_ts" => "2025-03-03T21:55:27Z"
# "hostname" => "www.giftkarte.com"

# class VTUAPI:
#     def __init__(self, api_key, public_key, secret_key):
    
#         self.base_url = BASE_URL
#         self.headers = {
#             "Accept": "application/json",
#             "api-key": api_key,
#             "Public-Key": public_key,
#             "Secret-key": secret_key,
#         }
#         self.session = Session()
#         self.session.headers.update(self.headers)
    
#     def getDataPlan(self, serviceID):
#         url = f"{self.base_url}service-variations?serviceID={serviceID}-data"
#         response = self.session.get(url)
#         return response.json()
    
#     def buydata(self, request_id, serviceID, billersCode, variation_code, amount, phone):
#         url = f"{self.base_url}pay"
#         payload = {
#             "request_id": request_id,
#             "serviceID": serviceID,
#             "billersCode":billersCode,
#             "variation_code":variation_code,
#             "amount": amount,
#             "phone": phone,
#         }
#         response = self.session.post(url, json=payload)
#         return response.json()


# def validate_gift_card(card_number, card_pin):
#     headers = {
#         'Authorization': f'Bearer {config("ZENDIT_API_KEY")}',
#         'Content-Type': 'application/json'
#     }
#     url = f'{config("ZENDIT_API_BASE_URL")}/giftcards/validate'

#     response = requests.post(url, json={
#         'card_number': card_number,
#         'card_pin': card_pin
#     }, headers=headers)

#     return response.json()  # Returns gift card validation status

# def scrape_website(request):
#     url = "https://example.com"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Extract specific elements
#     titles = soup.find_all('h2', class_='post-title')

#     extracted_titles = [title.get_text() for title in titles]

#     return extracted_titles
