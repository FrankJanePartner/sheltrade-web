from django.apps import AppConfig

"""
App Configuration for the Crypto App.

This module defines the configuration for the `Crypto` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Crypto`) for reference in Django's project settings.
- Ensures that signal handlers from the `Crypto.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `Crypto.signals` are loaded during app initialization.

"""

class CryptoConfig(AppConfig):
    """Configuration class for the Crypto app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'crypto'   # Defines the name of the app

