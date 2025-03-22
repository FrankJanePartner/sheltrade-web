from django.contrib import admin
from .models import TVSubscription, ElectricityPayment

"""
Admin configuration for managing TVSubscription and ElectricityPayment models in Django Admin.

This file registers the models to the Django admin panel, allowing administrators
 to view, add, update, and delete TV subscription and electricity payment records.

Modules:
    - admin: Django's built-in admin module for handling administrative tasks.
    - models: Imports TVSubscription and ElectricityPayment models from the current app.

Usage:
    After registering the models, they will be accessible in the Django Admin panel.
"""

# Registers the TVSubscription model to appear in the Django admin panel.
admin.site.register(TVSubscription)

# Registers the ElectricityPayment model to appear in the Django admin panel.
admin.site.register(ElectricityPayment)