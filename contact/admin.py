"""
Admin Configuration for the Contact App.

This module registers the `Contact` model with the Django admin site.
By registering the model, administrators can manage contact messages via the Django admin panel.

Features:
- Displays contact messages in the Django admin interface.
- Allows admin users to view, edit, and delete messages.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `Contact` model is automatically available in the Django admin dashboard after registration.
"""

from django.contrib import admin
from .models import Contact

# Register the Contact model in the Django admin panel
admin.site.register(Contact)
