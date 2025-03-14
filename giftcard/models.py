from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class GiftCard(models.Model):
    CARD_STATUSES = [
        ('pending', 'Pending Verification'),
        ('invalid', 'Invalid'),
        ('listed', 'Listed for Sale'),
        ('sold', 'Sold'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards', null=True)
    card_type = models.CharField(max_length=50, help_text=_("Brand/retailer name e.g., Amazon, Steam"))
    card_number = models.CharField(max_length=30, blank=True, null=True)
    card_pin = models.CharField(max_length=30, blank=True, null=True)
    card_code = models.CharField(max_length=20, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    condition = models.CharField(max_length=20, blank=True, null=True, help_text=_("Condition of the gift card (new, used, partially used)"))
    restrictions = models.TextField(blank=True, null=True, help_text=_("Any specific terms or restrictions"))
    uploaded_image = models.ImageField(upload_to='media/gift_cards/', default="media/defaults/gift-card.png", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=CARD_STATUSES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card_type} - {self.seller.username}"



class BuyGiftCard(models.Model):
    ESCROW_STATUSES = [
        ('held', 'Held'),
        ('released', 'Released'),
        ('refunded', 'Refunded')
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bought_cards', null=True)
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE, related_name='bought', null=True)
    escrow_status = models.CharField(max_length=10, choices=ESCROW_STATUSES, default='held')
    bought_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.gift_card.card_type} bought by {self.buyer.username}"
