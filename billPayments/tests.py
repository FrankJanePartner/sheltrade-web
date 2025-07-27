"""
Test module for the billPayments app.

This module contains unit tests for the billPayments app's functionality.
It includes basic tests for the TVSubscription and ElectricityPayment models.

Usage:
- Run these tests to verify basic billPayments app model behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import TVSubscription, ElectricityPayment
from .views import bills, get_tv_services, subscribe_tv, subs, pay_electricity

class BillPaymentsAppTests(TestCase):
    """
    Basic tests for the billPayments app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_tvsubscription_creation(self):
        """
        Test creating a TVSubscription instance and verify its fields.
        """
        tv_sub = TVSubscription.objects.create(
            user=self.user,
            provider='DSTV',
            smart_card_number='1234567890',
            amount=5000.00,
            status='pending'
        )
        self.assertEqual(tv_sub.provider, 'DSTV')
        self.assertEqual(tv_sub.smart_card_number, '1234567890')
        self.assertEqual(tv_sub.amount, 5000.00)
        self.assertEqual(tv_sub.status, 'pending')

    def test_electricitypayment_creation(self):
        """
        Test creating an ElectricityPayment instance and verify its fields.
        """
        elec_pay = ElectricityPayment.objects.create(
            user=self.user,
            provider='Ikeja Electric',
            meter_number='9876543210',
            meter_type='prepaid',
            amount=3000.00,
            status='pending'
        )
        self.assertEqual(elec_pay.provider, 'Ikeja Electric')
        self.assertEqual(elec_pay.meter_number, '9876543210')
        self.assertEqual(elec_pay.meter_type, 'prepaid')
        self.assertEqual(elec_pay.amount, 3000.00)
        self.assertEqual(elec_pay.status, 'pending')

    def test_bills_view(self):
        """
        Test the bills view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('billPayments:bills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billPayment/bills.html')

    def test_get_tv_services_view(self):
        """
        Test the get_tv_services view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('billPayments:get_tv_services'))
        self.assertIn(response.status_code, [200, 400])  # 400 if no serviceID param

    def test_subscribe_tv_view_post(self):
        """
        Test the subscribe_tv view POST request requires login and returns redirect or error.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('billPayments:subscribe_tv'), {})
        self.assertIn(response.status_code, [302, 400])  # Redirect or error due to missing data

    def test_subs_view(self):
        """
        Test the subs view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('billPayments:subs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billPayment/subscriptions.html')

    def test_pay_electricity_view_post(self):
        """
        Test the pay_electricity view POST request requires login and returns redirect or error.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('billPayments:pay-electricity'), {})
        self.assertIn(response.status_code, [302, 400])  # Redirect or error due to missing data

    def test_url_resolves(self):
        """
        Test that billPayments URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('billPayments:bills')).func, bills)
        self.assertEqual(resolve(reverse('billPayments:get_tv_services')).func, get_tv_services)
        self.assertEqual(resolve(reverse('billPayments:subscribe_tv')).func, subscribe_tv)
        self.assertEqual(resolve(reverse('billPayments:subs')).func, subs)
        self.assertEqual(resolve(reverse('billPayments:pay-electricity')).func, pay_electricity)
