"""
Test module for the sheltradeAdmin app.

This module contains unit tests for the sheltradeAdmin app's models.

Usage:
- Run these tests to verify basic sheltradeAdmin app model behavior.
"""

from django.test import TestCase
from .models import BankDetail

class SheltradeAdminAppTests(TestCase):
    """
    Basic tests for the sheltradeAdmin app.
    """

    def test_bankdetail_creation(self):
        """
        Test creating a BankDetail instance and verify its fields.
        """
        bank_detail = BankDetail.objects.create(
            bank_name='Test Bank',
            account_number='1234567890',
            account_holder_name='John Doe',
            currency='USD'
        )
        self.assertEqual(bank_detail.bank_name, 'Test Bank')
        self.assertEqual(bank_detail.account_number, '1234567890')
        self.assertEqual(bank_detail.account_holder_name, 'John Doe')
        self.assertEqual(bank_detail.currency, 'USD')
