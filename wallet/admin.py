"""
Admin Configuration for the Wallet App.

This module registers the `Wallet`, `Transaction`, `DepositNarration`, `Withdrawal`, and `WithdrawalAccount` models with the Django admin site.
By registering these models, administrators can manage wallets and transactions via the Django admin panel.

Features:
- Displays Wallet, Transaction, DepositNarration, Withdrawal, and WithdrawalAccount in the Django admin interface.
- Allows admin users to view, edit, and delete Wallets, Transactions, DepositNarrations, Withdrawals, and WithdrawalAccounts.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `Wallet`, `Transaction`, `DepositNarration`, `Withdrawal`, and `WithdrawalAccount` models are automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import Wallet, Transaction, DepositNarration, Withdrawal, WithdrawalAccount

# Register the Wallet model in the Django admin panel.
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(DepositNarration)
admin.site.register(Withdrawal)
admin.site.register(WithdrawalAccount)
