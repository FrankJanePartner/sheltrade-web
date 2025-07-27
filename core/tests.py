"""
Test module for the Core app.

This module contains unit tests for the Core app's functionality.
It includes basic tests for the Profile model.

Usage:
- Run these tests to verify basic Core app model behavior.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Profile
from .views import home, aboutus, dashboard, profile, preferred_currency, notification, notification_detail, mark_all_as_read, settings, phoneNumberLogin, addPhoneNumber, changeUserName, changeNames, legal

class CoreAppTests(TestCase):
    """
    Basic tests for the Core app.
    """

    def setUp(self):
        """
        Create a test user for foreign key relations and test client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_profile_creation(self):
        """
        Test creating a Profile instance and verify its default values.
        """
        profile = Profile.objects.create(user=self.user, preferredCurrency='USD')
        self.assertEqual(profile.preferredCurrency, 'USD')
        self.assertIsNone(profile.phone_Number)

    def test_home_view(self):
        """
        Test the home view returns status code 200.
        """
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_aboutus_view(self):
        """
        Test the aboutus view returns status code 200.
        """
        response = self.client.get(reverse('core:aboutus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/aboutus.html')

    def test_dashboard_view_redirects_for_anonymous(self):
        """
        Test that dashboard view redirects anonymous users to login.
        """
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_view_authenticated(self):
        """
        Test dashboard view for authenticated user returns 200.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')

    def test_url_resolves(self):
        """
        Test that core URLs resolve to correct view functions.
        """
        self.assertEqual(resolve(reverse('core:home')).func, home)
        self.assertEqual(resolve(reverse('core:aboutus')).func, aboutus)
        self.assertEqual(resolve(reverse('core:dashboard')).func, dashboard)
        self.assertEqual(resolve(reverse('core:profile')).func, profile)
        self.assertEqual(resolve(reverse('core:preferred_currency')).func, preferred_currency)
        self.assertEqual(resolve(reverse('core:notification')).func, notification)
        # For notification_detail, test with a dummy slug
        self.assertEqual(resolve('/core/notification_detail/dummy-slug').func, notification_detail)
        self.assertEqual(resolve(reverse('core:mark_all_as_read')).func, mark_all_as_read)
        self.assertEqual(resolve(reverse('core:settings')).func, settings)
        self.assertEqual(resolve(reverse('core:phoneNumberLogin')).func, phoneNumberLogin)
        self.assertEqual(resolve(reverse('core:addPhoneNumber')).func, addPhoneNumber)
        self.assertEqual(resolve(reverse('core:changeUserName')).func, changeUserName)
        self.assertEqual(resolve(reverse('core:changeNames')).func, changeNames)
        # For legal, test with a dummy slug
        self.assertEqual(resolve('/core/legal/dummy-slug/').func, legal)
