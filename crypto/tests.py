"""
Test module for the crypto app.

This module contains unit tests for the crypto app's functionality.
It includes basic tests for the UserAddress model and views.

Usage:
- Run these tests to verify basic crypto app model and view behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import UserAddress
from .views import buycrypto, sellcrypto, fetch_coin_price

class CryptoAppTests(TestCase):
    """
    Basic tests for the crypto app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_useraddress_creation(self):
        """
        Test creating a UserAddress instance and verify its fields.
        """
        user_address = UserAddress.objects.create(
            user=self.user,
            coin='Bitcoin',
            address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        )
        self.assertEqual(user_address.user, self.user)
        self.assertEqual(user_address.coin, 'Bitcoin')
        self.assertEqual(user_address.address, '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')

    def test_buycrypto_view(self):
        """
        Test the buycrypto view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('crypto:buycrypto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crypto/buycrypto.html')

    def test_sellcrypto_view(self):
        """
        Test the sellcrypto view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('crypto:sellcrypto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crypto/sellcrypto.html')

    def test_fetch_coin_price_view(self):
        """
        Test the fetch_coin_price view returns status code 400 without parameters.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('crypto:crypto-price'))
        self.assertEqual(response.status_code, 400)

    def test_url_resolves(self):
        """
        Test that crypto URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('crypto:buycrypto')).func, buycrypto)
        self.assertEqual(resolve(reverse('crypto:sellcrypto')).func, sellcrypto)
        self.assertEqual(resolve(reverse('crypto:crypto-price')).func, fetch_coin_price)
