from django.apps import AppConfig
import sys
import logging
logger = logging.getLogger(__name__)

"""
App Configuration for the Core App.

This module defines the configuration for the `Core` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Core`) for reference in Django's project settings.
- Ensures that signal handlers from the `core.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `core.signals` are loaded during app initialization.

"""

class CoreConfig(AppConfig):
    
    """Configuration class for the Core app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field 
    name = 'core'   # Defines the name of the app

    def ready(self):
        """
        Executes when the Django application is fully loaded.

        This method imports the `core.signals` module to ensure that any signal handlers 
        related to the Core app are registered and functional.
        
        Signals are used to execute code in response to model events like saving or deleting an object.
        """
        import core.signals  # Importing signal handlers to connect them to Django's signal framework

        # List of allowed models in 'app_label.modelname' format
        allowed_models = ['contact.Contact','gitcard.GiftCard', 'wallet.Deposit', 'wallet.Withdrawal', 'wallet.WithdrawalAccount']

        if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
            return  # Avoid running during migrations

        try:
            from django.contrib.auth.models import Group, Permission
            from django.contrib.contenttypes.models import ContentType
            from django.apps import apps

            staff_group, _ = Group.objects.get_or_create(name='Workers')

            # Clear all permissions first to avoid duplicates
            staff_group.permissions.clear()

            for model in apps.get_models():
                model_label = f"{model._meta.app_label}.{model.__name__}"
                content_type = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(content_type=content_type)

                if model_label in allowed_models:
                    # Grant view permission
                    view_perm = perms.filter(codename=f'view_{model.__name__.lower()}').first()
                    if view_perm:
                        staff_group.permissions.add(view_perm)
                        logger.debug(f"Added permission {view_perm.codename} to Workers group")

                    # Grant change permission - but field-level restrictions must be enforced elsewhere
                    change_perm = perms.filter(codename=f'change_{model.__name__.lower()}').first()
                    if change_perm:
                        staff_group.permissions.add(change_perm)
                        logger.debug(f"Added permission {change_perm.codename} to Workers group")

                    # Optionally, add add and delete permissions if needed
                    # add_perm = perms.filter(codename=f'add_{model.__name__.lower()}').first()
                    # delete_perm = perms.filter(codename=f'delete_{model.__name__.lower()}').first()
                    # if add_perm:
                    #     staff_group.permissions.add(add_perm)
                    # if delete_perm:
                    #     staff_group.permissions.add(delete_perm)

                else:
                    # Remove all permissions for models not in allowed list
                    for perm in perms:
                        if perm in staff_group.permissions.all():
                            staff_group.permissions.remove(perm)
                            logger.debug(f"Removed permission {perm.codename} from Workers group")

            # Note: Field-level update restrictions should be implemented in forms or views
            # using the allowed_update_fields dictionary above.

        except Exception as e:
            logger.warning(f"Skipping permission setup in Workers.ready() due to error: {e}")
