"""
Admin Configuration for the core App.

This module registers the `core` model with the Django admin site.
By registering the model, administrators can manage Profile and Notification via the Django admin panel.

Features:
- Displays Profile and Notification in the Django admin interface.
- Allows admin users to view, edit, and delete Profile and Notification.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `core` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from  .models import Profile, Notification

# Register the core model in the Django admin panel
admin.site.register(Profile)
admin.site.register(Notification)
