from rest_framework import viewsets

from billPayments.models import TVSubscription, ElectricityPayment
from contact.models import Contact, SheltradeSocialMedia, SheltradeContact
from core.models import Profile, Notification, Legal
from crypto.models import UserAddress
from giftcard.models import GiftCard
from mobileTopUp.models import SavedTransactionInfo
from sheltradeAdmin.models import BankDetail, CryptoWallet, TransactionCharge, CashBack, SheltradeTeam
from wallet.models import Wallet, Transaction, Deposit, WithdrawalAccount, Withdrawal

from .serializers import (
    TVSubscriptionSerializer,
    ElectricityPaymentSerializer,
    ContactSerializer,
    SheltradeSocialMediaSerializer,
    SheltradeContactSerializer,
    ProfileSerializer,
    NotificationSerializer,
    LegalSerializer,
    UserAddressSerializer,
    GiftCardSerializer,
    SavedTransactionInfoSerializer,
    BankDetailSerializer,
    CryptoWalletSerializer,
    TransactionChargeSerializer,
    CashBackSerializer,
    SheltradeTeamSerializer,
    WalletSerializer,
    TransactionSerializer,
    DepositSerializer,
    WithdrawalAccountSerializer,
    WithdrawalSerializer,
)

# ViewSets for billPayments app
class TVSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TVSubscription.objects.all()
    serializer_class = TVSubscriptionSerializer

class ElectricityPaymentViewSet(viewsets.ModelViewSet):
    queryset = ElectricityPayment.objects.all()
    serializer_class = ElectricityPaymentSerializer

# ViewSets for contact app
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class SheltradeSocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SheltradeSocialMedia.objects.all()
    serializer_class = SheltradeSocialMediaSerializer

class SheltradeContactViewSet(viewsets.ModelViewSet):
    queryset = SheltradeContact.objects.all()
    serializer_class = SheltradeContactSerializer

# ViewSets for core app
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class LegalViewSet(viewsets.ModelViewSet):
    queryset = Legal.objects.all()
    serializer_class = LegalSerializer

# ViewSets for crypto app
class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

# ViewSets for giftcard app
class GiftCardViewSet(viewsets.ModelViewSet):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer

# ViewSets for mobileTopUp app
class SavedTransactionInfoViewSet(viewsets.ModelViewSet):
    queryset = SavedTransactionInfo.objects.all()
    serializer_class = SavedTransactionInfoSerializer

# ViewSets for sheltradeAdmin app
class BankDetailViewSet(viewsets.ModelViewSet):
    queryset = BankDetail.objects.all()
    serializer_class = BankDetailSerializer

class CryptoWalletViewSet(viewsets.ModelViewSet):
    queryset = CryptoWallet.objects.all()
    serializer_class = CryptoWalletSerializer

class TransactionChargeViewSet(viewsets.ModelViewSet):
    queryset = TransactionCharge.objects.all()
    serializer_class = TransactionChargeSerializer

class CashBackViewSet(viewsets.ModelViewSet):
    queryset = CashBack.objects.all()
    serializer_class = CashBackSerializer

class SheltradeTeamViewSet(viewsets.ModelViewSet):
    queryset = SheltradeTeam.objects.all()
    serializer_class = SheltradeTeamSerializer

# ViewSets for wallet app
class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

class WithdrawalAccountViewSet(viewsets.ModelViewSet):
    queryset = WithdrawalAccount.objects.all()
    serializer_class = WithdrawalAccountSerializer

class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
