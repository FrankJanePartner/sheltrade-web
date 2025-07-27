from rest_framework import serializers

# Import models explicitly from each app
from billPayments.models import TVSubscription, ElectricityPayment
from contact.models import Contact, SheltradeSocialMedia, SheltradeContact
from core.models import Profile, Notification, Legal
from crypto.models import UserAddress
from giftcard.models import GiftCard
from mobileTopUp.models import SavedTransactionInfo
from sheltradeAdmin.models import BankDetail, CryptoWallet, TransactionCharge, CashBack, SheltradeTeam
from wallet.models import Wallet, Transaction, Deposit, WithdrawalAccount, Withdrawal

# Serializers for billPayments app
class TVSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVSubscription
        fields = '__all__'

class ElectricityPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityPayment
        fields = '__all__'

# Serializers for contact app
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class SheltradeSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheltradeSocialMedia
        fields = '__all__'

class SheltradeContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheltradeContact
        fields = '__all__'

# Serializers for core app
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legal
        fields = '__all__'

# Serializers for crypto app
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'

# Serializers for giftcard app
class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'

# Serializers for mobileTopUp app
class SavedTransactionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedTransactionInfo
        fields = '__all__'

# Serializers for sheltradeAdmin app
class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'

class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = '__all__'

class TransactionChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCharge
        fields = '__all__'

class CashBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBack
        fields = '__all__'

class SheltradeTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheltradeTeam
        fields = '__all__'

# Serializers for wallet app
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class WithdrawalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalAccount
        fields = '__all__'

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'
