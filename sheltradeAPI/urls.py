from django.urls import path, include, re_path
# from rest_framework.routers import DefaultRouter

from .views import (
    # CustomEmailVerificationSentView,
    # CustomVerifyEmailView,
    UserListAPIView,
    GetTVServices,
    SubscribeTV,
    PayElectricity,
    ContactViewSet,
    ContactDetailSet,
    ProfileView,
    PreferredCurrencyView,
    PhoneNumberView,
    PhoneNumberLoginView,
    NotificationListView,
    NotificationDetailView,
    MarkAllAsReadView,
    ChangeUsernameView,
    sell_crypto,
    buy_crypto,
    fetch_coin_price,
    GiftCardListView,
    GiftCardDetailView,
    CreateGiftCardView,
    UpdateGiftCardView,
    DeleteGiftCardView,
    buy_airtime,
    buy_data,
    fetch_data_plans,
    wallet,
    transactions,
    deposit,
    deposit_submit_view,
    withdrawal,
    withdrawal_submit_view,
    add_account,
)


app_name = 'sheltradeAPI'


urlpatterns = [
    # path('auth/registration/account-confirm-email/<key>/', CustomVerifyEmailView.as_view(), name='api_account_confirm_email'),
    # path('auth/registration/account-confirm-email/', CustomEmailVerificationSentView.as_view(), name='api_account_email_verification_sent'),

    # User API
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("change-username/", ChangeUsernameView.as_view(), name="change-username"),
    # Bill Payment API
    path("billpayment/tv-services/", GetTVServices.as_view(), name="get-tv-services"),
    path("billpayment/subscribe-tv/", SubscribeTV.as_view(), name="subscribe-tv"),
    path(
        "billpayment/pay-electricity/", PayElectricity.as_view(), name="pay-electricity"
    ),
    # Contact API
    path("contacts/", ContactViewSet.as_view(), name="contact"),
    path("contacts/<pk>", ContactDetailSet.as_view(), name="contact"),
    # Core API
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "preferred-currency/",
        PreferredCurrencyView.as_view(),
        name="preferred-currency",
    ),
    path("user-phone-number/", PhoneNumberView.as_view(), name="user-phone-number"),
    path(
        "login/phone_Number/",
        PhoneNumberLoginView.as_view(),
        name="phone_Number",
    ),
    # Notifications API
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path(
        "notifications/<slug:slug>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path(
        "notifications/mark-all/",
        MarkAllAsReadView.as_view(),
        name="mark-all-notifications",
    ),
    # Crypto API
    path("sell-crypto/", sell_crypto, name="sell-crypto"),
    path("buy-crypto/", buy_crypto, name="buy-crypto"),
    path("price-crypto/", fetch_coin_price, name="fetch-coin-price"),
    
    # Gift Card API
    path("giftcards/", GiftCardListView.as_view(), name="giftcard-list"),
    path(
        "giftcards/<slug:slug>/", GiftCardDetailView.as_view(), name="giftcard-detail"
    ),
    path("giftcards/create/", CreateGiftCardView.as_view(), name="giftcard-create"),
    path(
        "giftcards/<slug:slug>/update/",
        UpdateGiftCardView.as_view(),
        name="giftcard-update",
    ),
    path(
        "giftcards/<slug:slug>/delete/",
        DeleteGiftCardView.as_view(),
        name="giftcard-delete",
    ),
    # Mobile Top-Up API
    path("airtime/buy/", buy_airtime, name="buy-airtime"),
    path("data/buy/", buy_data, name="buy-data"),
    path("data/plans/", fetch_data_plans, name="fetch-data-plans"),
    # Wallet API
    path("wallet/", wallet, name="wallet"),
    path("transactions/", transactions, name="transactions"),
    path("deposit/", deposit, name="deposit"),
    path("deposit/submit/", deposit_submit_view, name="deposit-submit"),
    path("withdrawal/", withdrawal, name="withdrawal"),
    path("withdrawal/submit/", withdrawal_submit_view, name="withdrawal-submit"),
    path("withdrawal/add-account/", add_account, name="add-account"),
    # Include ViewSet URLs
    # path('', include(router.urls)),
]
