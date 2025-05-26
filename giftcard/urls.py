from django.urls import path
from .views import sell_gift_card, buy_gift_card, gift_card_details, list_gift_card, delete_gift_card

app_name = 'giftcard'

urlpatterns = [
    path('', list_gift_card, name='market'),
    path('buy/', buy_gift_card, name='buy_gift_card'),
    path('sell/', sell_gift_card, name='sell_gift_card'),
    path('<slug:slug>', gift_card_details, name='giftcard-details'),
    path('<slug:slug>/delete/', delete_gift_card, name='delete'),
]
