"""
Admin Configuration for the Giftcard App.

This module registers the `GiftCard` model with the Django admin site.
By registering the model, administrators can manage gift cards via the Django admin panel.

Features:
- Displays GiftCard in the Django admin interface.
- Allows admin users to view, edit, and delete GiftCards.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `GiftCard` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import GiftCard

# Register the GiftCard model in the Django admin panel
class GiftCardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("seller", "card_type"),}

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.status in ['Sold', 'Rejected']:
                # If deposit is already processed, make all fields readonly
                return [
                    'seller', 'buyer', 'slug', 'card_type', 'card_pin',
                    'expiration_date', 'condition', 'restrictions', 
                    'uploaded_image', 'price' 'status', 'uploaded_at',
                    'updated_at', 'sold_at'
                ]
            else:
                # Allow changing status, make the rest readonly
                return [
                    'seller', 'buyer', 'slug', 'card_type', 'card_pin',
                    'expiration_date', 'condition', 'restrictions', 
                    'uploaded_image', 'price', 'uploaded_at',
                    'updated_at', 'sold_at'
                ]
        return []

admin.site.register(GiftCard, GiftCardAdmin)
