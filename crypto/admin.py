"""
Admin Configuration for the Crypto App.

This module registers the `UserAddress` model with the Django admin site.
By registering the model, administrators can manage user wallet addresses via the Django admin panel.

Features:
- Displays UserAddress in the Django admin interface.
- Allows admin users to view, edit, and delete UserAddress.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `UserAddress` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import UserAddress

# Register the UserAddress model in the Django admin panel
admin.site.register(UserAddress)
