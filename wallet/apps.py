from django.apps import AppConfig
"""
App Configuration for the Wallet App.

This module defines the configuration for the `Wallet` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Wallet`) for reference in Django's project settings.
- Ensures that signal handlers from the `Wallet.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `Wallet.signals` are loaded during app initialization.

"""
class WalletConfig(AppConfig):
    """Configuration class for the Wallet app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'wallet'   # Defines the name of the app

    def ready(self):
        """
        Executes when the Django application is fully loaded.

        This method imports the `core.signals` module to ensure that any signal handlers 
        related to the Contact app are registered and functional.
        
        Signals are used to execute code in response to model events like saving or deleting an object.
        """
        import wallet.signals  # Importing signal handlers to connect them to Django's signal framework

