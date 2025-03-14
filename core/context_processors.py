from .models import Profile
from django.contrib.auth.models import User
from forex_python.converter import CurrencyCodes
import logging  # Importing the logging module to log information and errors
import requests  # Importing the requests module to make HTTP requests
import phonenumbers  # Importing phonenumbers for handling phone number formatting
from django_countries import countries  # Importing countries to get country data
from django_countries.data import COUNTRIES  # Correct import
import phonenumbers  # For phone number formatting



def get_currency_symbol(currency_code):
    c = CurrencyCodes()
    return c.get_symbol(currency_code)


def currency(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.filter(user=user).first()  # Retrieve the profile
        if profile:  # Check if profile exists
            currency_code = profile.preferredCurrency
            currency_symbol = get_currency_symbol(currency_code)
        else:
            currency_symbol = '₦'  # Fallback if no profile exists
    else:
        currency_symbol = '₦'  # Fallback for unauthenticated users

    context = {
        "currency_symbol": currency_symbol,
    }
    return context



def UserProfile(request):
    user = request.user
    if not user.is_authenticated:
        return {'profile': None}  # Return an empty profile context for unauthenticated users
    
    profile = Profile.objects.filter(user=user).first()  # Retrieve the profile if authenticated
    return {'profile': profile}


def countries(request):
    countries_list = list(COUNTRIES.items())  # Get the list of countries
    supported_countries = phonenumbers.SUPPORTED_REGIONS  # Get supported phone number regions
    country_codes = []  # Initialize a list for country codes

    # Get country codes and country names
    for country in supported_countries:  # Loop through supported countries
        country_code = phonenumbers.country_code_for_region(country)  # Get country code
        if country_code:  # If a country code is found
            country_codes.append((f"+{country_code}", country))  # Format (+Code, Country Name)

    # Sort the country codes numerically by removing the '+' sign for comparison
    sorted_country_codes = sorted(country_codes, key=lambda x: int(x[0].replace("+", "")))

    context = {
        'countries': countries_list,
        'country_codes': sorted_country_codes,
    }

    return context
