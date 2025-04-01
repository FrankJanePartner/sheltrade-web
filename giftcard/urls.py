from django.urls import path
from .views import sell_gift_card, buy_gift_card#, add_gift_card, buy_gift_card, market

app_name = 'giftcard'

urlpatterns = [
    path('', buy_gift_card, name='buy_gift_card'),
    path('sell/', sell_gift_card, name='sell_gift_card'),
    # path('add-gift-card/', add_gift_card, name='add_gift_card'),
    # path('buy_gift_card/', buy_gift_card, name='buy_gift_card'),
    # path('market/', market, name='market'),
]

