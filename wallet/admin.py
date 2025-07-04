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
from .models import Wallet, Transaction, Deposit, Withdrawal, WithdrawalAccount
from mptt.admin import MPTTModelAdmin

class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.status in ['Approved', 'Rejected']:
                # If deposit is already processed, make all fields readonly
                return [
                    'user', 'transaction', 'naration',
                    'amount', 'proof_of_payment', 'status'
                ]
            else:
                # Allow changing status, make the rest readonly
                return [
                    'user', 'transaction', 'naration',
                    'amount', 'proof_of_payment'
                ]
        return []


class WithdrawalAdmin(admin.TabularInline):
    list_display = ('user', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [
        Withdrawal
    ]

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.status in ['Sent', 'Declined']:
                return [
                    'user', 'transaction',
                    'amount', 'status'
                ]
            else:
                return [
                    'user', 'transaction', 'amount'
                ]
        return []


class WithdrawalAccountAdmin(admin.ModelAdmin):
    model = WithdrawalAccount


admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal)
admin.site.register(WithdrawalAccount, WithdrawalAccountAdmin)

