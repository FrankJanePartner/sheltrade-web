"""
Admin Configuration for the Giftcard App.

This module registers the `GiftCard` model with the Django admin site.
By registering the model, administrators can manage gift cards via the Django admin panel.

Features:
- Displays GiftCard in the Django admin interface.
- Allows admin users to view, edit, and delete GiftCards.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `GiftCard` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import GiftCard

# Register the GiftCard model in the Django admin panel
admin.site.register(GiftCard)
