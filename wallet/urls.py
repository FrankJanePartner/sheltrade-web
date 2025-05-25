from django.urls import path
from .views import wallet, deposit, withdrawal, AddAccount, transactions

app_name='wallet'

urlpatterns = [
    path('', wallet, name='wallet'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdrawal, name='withdraw'),
    path('add_account/', AddAccount, name='add_account'),
    path('transactions/', transactions, name='transactions'),
]
