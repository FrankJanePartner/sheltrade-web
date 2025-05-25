"""
Admin Configuration for the SheltradeAdmin App.

This module registers the `SheltradeAdmin` model with the Django admin site.
By registering the model, administrators can manage BankDetails, CryptoWallets, TransactionCharges, SheltradeTeam and CashBacks via the Django admin panel.

Features:
- Displays BankDetails, CryptoWallets, TransactionCharges, SheltradeTeam and CashBacks in the Django admin interface.
- Allows admin users to view, edit, and delete BankDetails, CryptoWallets, TransactionCharges, SheltradeTeam and CashBacks.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `SheltradeAdmin` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import BankDetail, CryptoWallet, TransactionCharge, CashBack, SheltradeTeam

# Register the SheltradeAdmin model in the Django admin panel
admin.site.register(BankDetail)
admin.site.register(CryptoWallet)
admin.site.register(TransactionCharge)
admin.site.register(CashBack)
admin.site.register(SheltradeTeam)