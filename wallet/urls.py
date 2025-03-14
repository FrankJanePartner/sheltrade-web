from django.urls import path
from .views import wallet, deposit, deposit_submit_view, withdrawal, withdrawal_submit_view, AddAccount, transactions

app_name='wallet'

urlpatterns = [
    path('', wallet, name='wallet'),
    path('deposit/', deposit, name='deposit'),
    path('deposit_submit_view/', deposit_submit_view, name='deposit_submit_view'),
    path('withdraw/', withdrawal, name='withdraw'),
    path('withdrawal_submit_view/', withdrawal_submit_view, name='withdrawal_submit_view'),
    path('add_account/', AddAccount, name='add_account'),
    path('transactions/', transactions, name='transactions'),
]
