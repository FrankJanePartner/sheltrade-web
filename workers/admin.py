"""
Admin Configuration for the Workers App.

This module registers the `Workers` model with the Django admin site.
By registering the model, administrators can manage Workers Activities via the Django admin panel.

Features:
- Displays Workers Activities in the Django admin interface.
- Allows admin users to view, edit, and delete activities.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `Workers` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import WorkersActivity

# Register the Workers model in the Django admin panel
admin.site.register(WorkersActivity)
