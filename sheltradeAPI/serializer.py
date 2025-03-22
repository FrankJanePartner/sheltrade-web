from rest_framework import serializers
from allauth.account.utils import send_email_confirmation
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from billPayments.models import TVSubscription, ElectricityPayment
from contact.models import Contact
from core.models import Profile, Notification
from crypto.models import UserAddress
from giftcard.models import GiftCard, BuyGiftCard
from mobileTopUp.models import SavedTransactionInfo
from wallet.models import Wallet, Transaction, DepositNarration, Withdrawal, WithdrawalAccount
# from workers.models import
User = get_user_model()

# dj_rest_auth
class CustomRegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        user.save()

# User model Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# billPayments app serializer
class TVSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVSubscription
        fields = '__all__'


class ElectricityPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityPayment
        fields = '__all__'


# contact app serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# core app serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# crypto app serializer
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


# giftcard app serializer
class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'


class BuyGiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyGiftCard
        fields = '__all__'


# mobileTopUp model Serializer
class SavedTransactionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# wallet app serializer
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class DepositNarrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositNarration
        fields = '__all__'


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'


class WithdrawalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalAccount
        fields = '__all__'

# workers app serializer
# class WorkersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Workers
#         fields = '__all__'
