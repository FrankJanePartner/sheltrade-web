from django.apps import AppConfig
"""
App Configuration for the SheltradeAPI App.

This module defines the configuration for the `SheltradeAPI` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`SheltradeAPI`) for reference in Django's project settings.
- Ensures that signal handlers from the `SheltradeAPI.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `SheltradeAPI.signals` are loaded during app initialization.

"""

class SheltradeapiConfig(AppConfig):
    """Configuration class for the SheltradeAPI app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'sheltradeAPI'   # Defines the name of the app
