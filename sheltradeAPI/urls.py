from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TVSubscriptionViewSet,
    ElectricityPaymentViewSet,
    ContactViewSet,
    SheltradeSocialMediaViewSet,
    SheltradeContactViewSet,
    ProfileViewSet,
    NotificationViewSet,
    LegalViewSet,
    UserAddressViewSet,
    GiftCardViewSet,
    SavedTransactionInfoViewSet,
    BankDetailViewSet,
    CryptoWalletViewSet,
    TransactionChargeViewSet,
    CashBackViewSet,
    SheltradeTeamViewSet,
    WalletViewSet,
    TransactionViewSet,
    DepositViewSet,
    WithdrawalAccountViewSet,
    WithdrawalViewSet,
)

router = DefaultRouter()
router.register(r'tvsubscriptions', TVSubscriptionViewSet)
router.register(r'electricitypayments', ElectricityPaymentViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'sheltradesocialmedias', SheltradeSocialMediaViewSet)
router.register(r'sheltradecontacts', SheltradeContactViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'legals', LegalViewSet)
router.register(r'useraddresses', UserAddressViewSet)
router.register(r'giftcards', GiftCardViewSet)
router.register(r'savedtransactioninfos', SavedTransactionInfoViewSet)
router.register(r'bankdetails', BankDetailViewSet)
router.register(r'cryptowallets', CryptoWalletViewSet)
router.register(r'transactioncharges', TransactionChargeViewSet)
router.register(r'cashbacks', CashBackViewSet)
router.register(r'sheltradeteams', SheltradeTeamViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'deposits', DepositViewSet)
router.register(r'withdrawalaccounts', WithdrawalAccountViewSet)
router.register(r'withdrawals', WithdrawalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
