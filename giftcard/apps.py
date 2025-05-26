from django.apps import AppConfig
"""
App Configuration for the Giftcard App.

This module defines the configuration for the `Giftcard` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Giftcard`) for reference in Django's project settings.
- Ensures that signal handlers from the `Giftcard.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `Giftcard.signals` are loaded during app initialization.

"""

class GiftcardConfig(AppConfig):
    """Configuration class for the Giftcard app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'giftcard'   # Defines the name of the app


    def ready(self):
        import giftcard.signals  # Importing signal handlers to connect them to Django's signal framework