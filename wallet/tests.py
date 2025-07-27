"""
Test module for the wallet app.

This module contains unit tests for the wallet app's functionality.
It includes basic tests for the Wallet model and views.

Usage:
- Run these tests to verify basic wallet app model and view behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Wallet
from .views import wallet, deposit, withdrawal, AddAccount, transactions

class WalletAppTests(TestCase):
    """
    Basic tests for the wallet app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.client = Client()

    def test_wallet_creation(self):
        """
        Test creating a Wallet instance and verify its fields.
        """
        wallet = Wallet.objects.create(
            user=self.user,
            balance=100.00,
            cashback=10.00
        )
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.balance, 100.00)
        self.assertEqual(wallet.cashback, 10.00)

    def test_wallet_view(self):
        """
        Test the wallet view returns status code 200.
        """
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('wallet:wallet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/wallet.html')

    def test_deposit_view(self):
        """
        Test the deposit view returns status code 200.
        """
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('wallet:deposit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/deposite.html')

    def test_withdrawal_view(self):
        """
        Test the withdrawal view returns status code 200.
        """
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('wallet:withdraw'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/withdraw.html')

    def test_add_account_view(self):
        """
        Test the AddAccount view returns status code 200.
        """
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('wallet:add_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/AddWithdrawalAccount.html')

    def test_transactions_view(self):
        """
        Test the transactions view returns status code 200.
        """
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('wallet:transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/transactions.html')

    def test_url_resolves(self):
        """
        Test that wallet URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('wallet:wallet')).func, wallet)
        self.assertEqual(resolve(reverse('wallet:deposit')).func, deposit)
        self.assertEqual(resolve(reverse('wallet:withdraw')).func, withdrawal)
        self.assertEqual(resolve(reverse('wallet:add_account')).func, AddAccount)
        self.assertEqual(resolve(reverse('wallet:transactions')).func, transactions)
