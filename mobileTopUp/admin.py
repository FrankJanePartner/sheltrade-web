"""
Admin Configuration for the MobileTopUp App.

This module registers the `MobileTopUp` model with the Django admin site.
By registering the model, administrators can manage SavedTransactionInfo via the Django admin panel.

Features:
- Displays SavedTransactionInfo in the Django admin interface.
- Allows admin users to view, edit, and delete SavedTransactionInfos.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `MobileTopUp` model is automatically available in the Django admin dashboard after registration.
"""

from django.contrib import admin
from .models import SavedTransactionInfo

# Register the MobileTopUp model in the Django admin panel
admin.site.register(SavedTransactionInfo)
