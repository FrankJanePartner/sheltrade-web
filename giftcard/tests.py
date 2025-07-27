"""
Test module for the giftcard app.

This module contains unit tests for the giftcard app's functionality.
It includes basic tests for the GiftCard model and views.

Usage:
- Run these tests to verify basic giftcard app model and view behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import GiftCard
from .views import sell_gift_card, buy_gift_card, gift_card_details, list_gift_card, delete_gift_card

class GiftCardAppTests(TestCase):
    """
    Basic tests for the giftcard app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_giftcard_creation(self):
        """
        Test creating a GiftCard instance and verify its fields.
        """
        giftcard = GiftCard.objects.create(
            seller=self.user,
            card_type='Amazon',
            card_pin='1234-5678-9012',
            price=1000.00,
            status='Pending'
        )
        self.assertEqual(giftcard.seller, self.user)
        self.assertEqual(giftcard.card_type, 'Amazon')
        self.assertEqual(giftcard.card_pin, '1234-5678-9012')
        self.assertEqual(giftcard.price, 1000.00)
        self.assertEqual(giftcard.status, 'Pending')

    def test_list_gift_card_view(self):
        """
        Test the list_gift_card view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('giftcard:market'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'giftcard/giftcard_list.html')

    def test_buy_gift_card_view(self):
        """
        Test the buy_gift_card view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('giftcard:buy_gift_card'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'giftcard/buygiftcard.html')

    def test_sell_gift_card_view(self):
        """
        Test the sell_gift_card view returns status code 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('giftcard:sell_gift_card'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'giftcard/sellgiftcard.html')

    def test_gift_card_details_view(self):
        """
        Test the gift_card_details view returns status code 200.
        """
        giftcard = GiftCard.objects.create(
            seller=self.user,
            card_type='Amazon',
            card_pin='1234-5678-9012',
            price=1000.00,
            status='listed',
            slug='test-slug'
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('giftcard:giftcard-details', args=[giftcard.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'giftcard/giftcard_details.html')

    def test_delete_gift_card_view(self):
        """
        Test the delete_gift_card view returns status code 200.
        """
        giftcard = GiftCard.objects.create(
            seller=self.user,
            card_type='Amazon',
            card_pin='1234-5678-9012',
            price=1000.00,
            status='listed',
            slug='test-slug-delete'
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('giftcard:delete', args=[giftcard.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'giftcard/confirm_delete.html')

    def test_url_resolves(self):
        """
        Test that giftcard URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('giftcard:market')).func, list_gift_card)
        self.assertEqual(resolve(reverse('giftcard:buy_gift_card')).func, buy_gift_card)
        self.assertEqual(resolve(reverse('giftcard:sell_gift_card')).func, sell_gift_card)
        self.assertEqual(resolve('/giftcard/test-slug').func, gift_card_details)
        self.assertEqual(resolve('/giftcard/test-slug-delete/delete/').func, delete_gift_card)
