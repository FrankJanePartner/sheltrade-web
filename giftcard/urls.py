from django.urls import path
from .views import sellgiftcard, buygiftcard, add_gift_card, buy_gift_card, market

app_name = 'giftcard'

urlpatterns = [
    path('', buygiftcard, name='buygiftcard'),
    path('sell/', sellgiftcard, name='sellgiftcard'),
    path('add-gift-card/', add_gift_card, name='add_gift_card'),
    path('buy_gift_card/', buy_gift_card, name='buy_gift_card'),
    path('market/', market, name='market'),
]

