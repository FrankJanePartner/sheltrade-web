from django.urls import path
from .views import buycrypto, sellcrypto, fetch_coin_price

app_name = 'crypto'

urlpatterns = [
    path('', buycrypto, name='buycrypto'),
    path('sellcrypto/', sellcrypto, name='sellcrypto'),
    path("crypto-price/", fetch_coin_price, name="crypto-price"),
]
