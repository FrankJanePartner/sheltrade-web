import json
import requests
from requests import Session
from pprint import pprint as pp
import random
import string
from datetime import datetime
from requests.auth import HTTPBasicAuth
import pytz

# Base URL for VTpass API (sandbox environment for testing)
BASE_URL = "https://sandbox.vtpass.com/api/"
VT_EMAIL = "partnermarvel55@gmail.com"  # Replace with your Vtpass email
VT_PASSWORD = "Tygeropartner@55"        # Replace with your Vtpass password

class VTUBILLSAPI:
    """
    A class to interact with the VTpass API for various bill payment services.
    Provides methods for:
    - Fetching available services
    - Verifying smart card numbers and meter numbers
    - Changing and renewing TV subscription plans
    - Paying for prepaid and postpaid electricity meters
    """

    def __init__(self, username, password):
        """
        Initializes the VTUBILLSAPI class with authentication.

        Args:
            username (str): VTpass username (email).
            password (str): VTpass password.
        """
        self.base_url = BASE_URL
        self.auth = HTTPBasicAuth(username, password)  # Set up Basic Authentication
        self.session = Session()
        self.session.auth = self.auth

    @staticmethod
    def generate_request_id(suffix_length=10):
        """
        Generates a unique request ID using the current timestamp and a random string.
        
        Args:
            suffix_length (int): Length of the random suffix (default is 10).
        
        Returns:
            str: Unique request ID.
        """
        lagos_tz = pytz.timezone('Africa/Lagos')
        now = datetime.now(lagos_tz)
        timestamp = now.strftime('%Y%m%d%H%M')  # Format: YYYYMMDDHHMM
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=suffix_length))
        return f"{timestamp}{suffix}"
    
    def getServices(self, serviceID):
        """
        Fetches available variations for a given service ID (e.g., TV subscriptions, electricity providers).
        
        Args:
            serviceID (str): The ID of the service.
        
        Returns:
            dict: JSON response containing service variations.
        """
        url = f"{self.base_url}service-variations?serviceID={serviceID}"
        response = self.session.get(url)
        return response.json()
    
    def verifySCNumber(self, billersCode, serviceID):
        """
        Verifies the smart card number for TV subscriptions.
        
        Args:
            billersCode (str): Smart card number to verify.
            serviceID (str): Service provider ID.
        
        Returns:
            dict: JSON response confirming the verification status.
        """
        url = f"{self.base_url}merchant-verify"
        payload = {
            "billersCode": billersCode,
            "serviceID": serviceID,
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def changePlan(self, request_id, serviceID, billersCode, variation_code, amount, phone, subscription_type, quantity):
        """
        Changes a TV subscription plan.
        
        Args:
            request_id (str): Unique request ID.
            serviceID (str): Service provider ID.
            billersCode (str): Smart card number.
            variation_code (str): Package variation code.
            amount (float): Amount to be paid.
            phone (str): User phone number.
            subscription_type (str): Type of subscription.
            quantity (int): Quantity of subscription.
        
        Returns:
            dict: JSON response containing transaction details.
        """
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
        """
        Renews an existing TV subscription plan.
        """
        return self.changePlan(request_id, serviceID, billersCode, variation_code, amount, phone, subscription_type, quantity)

    def verifyMeter(self, billersCode, serviceID, metertype):
        """
        Verifies an electricity meter number.
        
        Args:
            billersCode (str): Meter number.
            serviceID (str): Electricity provider ID.
            metertype (str): Meter type (prepaid or postpaid).
        
        Returns:
            dict: JSON response confirming verification status.
        """
        url = f"{self.base_url}merchant-verify"
        payload = {
            "billersCode": billersCode,
            "serviceID": serviceID,
            "type": metertype,
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def prepaidMeter(self, request_id, serviceID, billersCode, variation_code, amount, phone):
        """
        Pays for a prepaid electricity meter.
        """
        return self.changePlan(request_id, serviceID, billersCode, variation_code, amount, phone, None, 1)
        
    def postpaidMeter(self, request_id, serviceID, billersCode, variation_code, amount, phone):
        """
        Pays for a postpaid electricity meter.
        """
        return self.changePlan(request_id, serviceID, billersCode, variation_code, amount, phone, None, 1)
