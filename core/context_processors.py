from .models import Profile
from django.contrib.auth.models import User
from forex_python.converter import CurrencyCodes
import logging  # Importing the logging module to log information and errors
import requests  # Importing the requests module to make HTTP requests
import phonenumbers  # Importing phonenumbers for handling phone number formatting
from django_countries import countries  # Importing countries to get country data
from django_countries.data import COUNTRIES  # Correct import


def get_currency_symbol(currency_code):
    """
    Get the currency symbol for a given currency code.

    Args:
        currency_code (str): The ISO currency code (e.g., 'USD', 'EUR').

    Returns:
        str: The currency symbol corresponding to the currency code.
    """
    c = CurrencyCodes()
    return c.get_symbol(currency_code)


def currency(request):
    """
    Context processor to add the currency symbol to the template context.

    Determines the currency symbol based on the authenticated user's profile.
    Falls back to the Nigerian Naira symbol (₦) if no profile or user is unauthenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary with the key 'currency_symbol' for template context.
    """
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
    """
    Context processor to add the user's profile to the template context.

    Returns None for unauthenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary with the key 'profile' for template context.
    """
    user = request.user
    if not user.is_authenticated:
        return {'profile': None}  # Return an empty profile context for unauthenticated users
    
    profile = Profile.objects.filter(user=user).first()  # Retrieve the profile if authenticated
    return {'profile': profile}


def countries(request):
    """
    Context processor to add country data and phone number country codes to the template context.

    Provides a list of countries and a sorted list of country codes with their region names,
    useful for phone number input fields.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary with keys 'countries' and 'country_codes' for template context.
    """
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
