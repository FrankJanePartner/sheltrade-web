from django.apps import AppConfig
"""
App Configuration for the Workers App.

This module defines the configuration for the `Workers` Django app.
It specifies default settings for the app and ensures necessary signal handlers are imported when the app is ready.

Features:
- Sets `default_auto_field` to `BigAutoField` for automatic primary key fields.
- Defines the app name (`Workers`) for reference in Django's project settings.
- Ensures that signal handlers from the `Workers.signals` module are imported when the app is ready.

Usage:
- This configuration is automatically applied when Django starts.
- Signals registered in `Workers.signals` are loaded during app initialization.

"""

class WorkersConfig(AppConfig):
    """Configuration class for the Workers app."""
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type
    name = 'workers'   # Defines the name of the app

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.apps import apps

        staff_group, _ = Group.objects.get_or_create(name='Workers')

        for model in apps.get_models():
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)

            for perm in perms:
                if "view" in perm.codename or "change" in perm.codename:
                    staff_group.permissions.add(perm)
