from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile
from wallet.models import Wallet

class UserRegistrationIntegrationTest(TestCase):
    def test_user_registration_creates_profile_and_wallet(self):
        # Create a new user
        user = User.objects.create_user(username='integrationuser', password='testpass123')
        # Check that Profile is created
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists, "Profile should be created for new user")
        # Check that Wallet is created with default balance 0.00
        wallet = Wallet.objects.filter(user=user).first()
        self.assertIsNotNone(wallet, "Wallet should be created for new user")
        if wallet is not None:
            self.assertEqual(wallet.balance, 0.00, "Wallet balance should be 0.00 for new user")
