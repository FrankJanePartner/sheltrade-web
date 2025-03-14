import json
import requests
from requests import Session
from pprint import pprint as pp
import random
import string
from datetime import datetime
from requests.auth import HTTPBasicAuth
import pytz


BASE_URL = "https://sandbox.vtpass.com/api/"
VT_EMAIL = "partnermarvel55@gmail.com"  # Replace with your Vtpass email
VT_PASSWORD = "Tygeropartner@55"        # Replace with your Vtpass password


class VTUBILLSAPI:
    def __init__(self, username, password):
    
        self.base_url = BASE_URL
        self.auth = HTTPBasicAuth(username, password)  # Set up Basic Auth
        self.session = Session()
        self.session.auth = self.auth


    @staticmethod
    def generate_request_id(suffix_length=10):
        """Generate a unique request ID."""
        lagos_tz = pytz.timezone('Africa/Lagos')
        now = datetime.now(lagos_tz)
        timestamp = now.strftime('%Y%m%d%H%M')
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=suffix_length))
        return f"{timestamp}{suffix}"
    

    def getServices(self, serviceID):
        url = f"{self.base_url}service-variations?serviceID={serviceID}"
        response = self.session.get(url)
        return response.json()
    
    def verifySCNumber(self, billersCode, serviceID):
        url = f"{self.base_url}merchant-verify"
        payload = {
            "billersCode": billersCode,
            "serviceID": serviceID,
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def changePlan(self, request_id, serviceID, billersCode, variation_code, amount, phone, subscription_type, quantity):
        url = f"{self.base_url}pay"
        payload = {
            "request_id": request_id,
            "serviceID": serviceID,
            "billersCode": billersCode,
            "variation_code": variation_code,
            "amount": amount,
            "phone": phone,
            "subscription_type": subscription_type,
            "quantity": quantity
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def renewPlan(self, request_id, serviceID, billersCode, variation_code, amount, phone, subscription_type, quantity):
            url = f"{self.base_url}pay"
            payload = {
                "request_id": request_id,
                "serviceID": serviceID,
                "billersCode": billersCode,
                "variation_code": variation_code,
                "amount": amount,
                "phone": phone,
                "subscription_type": subscription_type,
                "quantity": quantity
            }
            response = self.session.post(url, json=payload)
            return response.json()

    def verifyMeter(self, billersCode, serviceID, metertype):
        url = f"{self.base_url}merchant-verify"
        payload = {
            "billersCode": billersCode,
            "serviceID": serviceID,
            "type": metertype,
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def prepaidMeter(self, request_id, serviceID, billersCode, variation_code, amount, phone):
            url = f"{self.base_url}pay"
            payload = {
                "request_id": request_id,
                "serviceID": serviceID,
                "billersCode": billersCode,
                "variation_code": variation_code,
                "amount": amount,
                "phone": phone,
            }
            response = self.session.post(url, json=payload)
            return response.json()
        
    def postpaidMeter(self, request_id, serviceID, billersCode, variation_code, amount, phone):
            url = f"{self.base_url}pay"
            payload = {
                "request_id": request_id,
                "serviceID": serviceID,
                "billersCode": billersCode,
                "variation_code": variation_code,
                "amount": amount,
                "phone": phone,
            }
            response = self.session.post(url, json=payload)
            return response.json()
