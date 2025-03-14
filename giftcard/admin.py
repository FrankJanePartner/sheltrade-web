from django.contrib import admin
from .models import GiftCard

# Register your models here.
admin.site.register(GiftCard)



# class GiftCardAdmin(admin.ModelAdmin):
#     # Specify the fields to display in the list view
#     list_display = ('card_type', 'seller', 'price', 'status', 'created_at')
    
#     # Add filters for the admin panel
#     list_filter = ('status', 'condition', 'created_at')
    
#     # Add a search bar
#     search_fields = ('card_type', 'seller__username', 'price')
    
#     # Customize the form layout
#     fieldsets = (
#         (None, {
#             'fields': ('seller', 'card_type', 'card_number', 'card_pin', 'card_code')
#         }),
#         ('Details', {
#             'fields': ('expiration_date', 'condition', 'restrictions', 'uploaded_image', 'price', 'status')
#         }),
#     )
    
#     # Optionally, you can customize the ordering
#     ordering = ('-created_at',)