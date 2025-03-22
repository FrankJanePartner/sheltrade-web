"""
Admin Configuration for the Wallet App.

This module registers the `Wallet` model with the Django admin site.
By registering the model, administrators can manage Wallet, Transaction, DepositNarations, Withdrawal and WithdrawalAccount via the Django admin panel.

Features:
- Displays Wallet, Transaction, DepositNarations, Withdrawal and WithdrawalAccount in the Django admin interface.
- Allows admin users to view, edit, and delete Wallets, Transactions, DepositNarations, Withdrawals and WithdrawalAccounts.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `Wallet` model is automatically available in the Django admin dashboard after registration.
"""

from django.contrib import admin
from .models import Wallet, Transaction, DepositNarations, Withdrawal, WithdrawalAccount

# Register the Wallet model in the Django admin panel.
admin.site.register(Wallet)
admin.site.register(Withdrawal)
admin.site.register(Transaction)
admin.site.register(DepositNarations)
admin.site.register(WithdrawalAccount)