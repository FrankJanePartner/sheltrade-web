from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from core.models import Profile
from wallet.models import Wallet
from core.signals import create_user_profile, create_worker_group
from django.db.models.signals import post_save, post_migrate
from unittest.mock import patch

class SignalTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('core.signals.RequestMiddleware.get_request')
    def test_create_user_profile_signal(self, mock_get_request):
        # Mock request with admin user add path
        mock_get_request.return_value = self.factory.get('/admin/auth/user/add/')

        user = User.objects.create(username='testuser', is_staff=False, is_superuser=False)
        # Profile and Wallet should be created
        profile = Profile.objects.filter(user=user).first()
        wallet = Wallet.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertIsNotNone(wallet)
        # User should be staff because created via admin add page
        user.refresh_from_db()
        self.assertTrue(user.is_staff)
        # User should be in Workers group
        self.assertTrue(user.groups.filter(name='Workers').exists())

    @patch('core.signals.RequestMiddleware.get_request')
    def test_create_user_profile_signal_non_admin(self, mock_get_request):
        # Mock request with non-admin path
        mock_get_request.return_value = self.factory.get('/some/other/path/')

        user = User.objects.create(username='testuser2', is_staff=False, is_superuser=False)
        profile = Profile.objects.filter(user=user).first()
        wallet = Wallet.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertIsNotNone(wallet)
        user.refresh_from_db()
        # User should not be staff
        self.assertFalse(user.is_staff)
        # User should be in Customers group
        self.assertTrue(user.groups.filter(name='Customers').exists())

    def test_create_worker_group_signal(self):
        # Before signal, delete Workers group if exists
        Group.objects.filter(name='Workers').delete()
        # Call the signal handler manually
        create_worker_group(sender=None)
        # Workers group should now exist
        self.assertTrue(Group.objects.filter(name='Workers').exists())
