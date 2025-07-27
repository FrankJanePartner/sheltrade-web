"""
Test module for the mobileTopUp app.

This module contains unit tests for the mobileTopUp app's functionality.
It includes basic tests for the SavedTransactionInfo model and views.

Usage:
- Run these tests to verify basic mobileTopUp app model and view behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import SavedTransactionInfo
from .views import buyairtime, buydata, fetch_data_plans

class MobileTopUpAppTests(TestCase):
    """
    Basic tests for the mobileTopUp app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_savedtransactioninfo_creation(self):
        """
        Test creating a SavedTransactionInfo instance and verify its fields.
        """
        transaction_info = SavedTransactionInfo.objects.create(
            user=self.user,
            phone_number='08012345678',
            provider='MTN'
        )
        self.assertEqual(transaction_info.user, self.user)
        self.assertEqual(transaction_info.phone_number, '08012345678')
        self.assertEqual(transaction_info.provider, 'MTN')

    def test_buyairtime_view(self):
        """
        Test the buyairtime view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('mobileTopUp:buyairtime'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mobileTopup/buyairtime.html')

    def test_buydata_view(self):
        """
        Test the buydata view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('mobileTopUp:buydata'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mobileTopup/buydata.html')

    def test_fetch_data_plans_view(self):
        """
        Test the fetch_data_plans view returns status code 400 without parameters.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('mobileTopUp:fetch_data_plans'))
        self.assertEqual(response.status_code, 400)

    def test_url_resolves(self):
        """
        Test that mobileTopUp URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('mobileTopUp:buyairtime')).func, buyairtime)
        self.assertEqual(resolve(reverse('mobileTopUp:buydata')).func, buydata)
        self.assertEqual(resolve(reverse('mobileTopUp:fetch_data_plans')).func, fetch_data_plans)
