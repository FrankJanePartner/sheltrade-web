from django.apps import AppConfig
"""
App Configuration for the Mobiletopup App.

This module defines the configuration for the `Mobiletopup` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Mobiletopup`) for reference in Django's project settings.
- Ensures that signal handlers from the `Mobiletopup.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `Mobiletopup.signals` are loaded during app initialization.

"""
class MobiletopupConfig(AppConfig):
    """Configuration class for the Mobiletopup app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'mobileTopUp'   # Defines the name of the app
