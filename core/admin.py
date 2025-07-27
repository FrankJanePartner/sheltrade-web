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

# Import the Django admin module to enable model registration and customization
from django.contrib import admin

# Import the Profile, Notification, and Legal models from the current app's models module
from  .models import Profile, Notification, Legal

# Register the Legal model with the Django admin site using a custom admin class
@admin.register(Legal)
class LegalAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Legal model.

    This class customizes the admin interface for the Legal model.
    It prepopulates the 'slug' field based on the 'name' field to simplify data entry.
    """
    # Automatically fill the 'slug' field in the admin form based on the 'name' field
    prepopulated_fields = {'slug': ('name',)}


# Register the Profile model with the default admin interface
# This allows admin users to view, add, edit, and delete Profile instances
admin.site.register(Profile)

# Register the Notification model with the default admin interface
# This allows admin users to manage Notification instances via the admin panel
admin.site.register(Notification)
