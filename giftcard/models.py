from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class GiftCard(models.Model):
    """
    Represents a gift card listed for sale by users.

    This model stores information about gift cards, including their type, 
    number, pin, code, expiration date, condition, restrictions, and price.

    Attributes:
        seller (User): The user who is selling the gift card.
        card_type (str): The type of the gift card (e.g., Amazon, iTunes).
        card_number (str): The card number of the gift card.
        card_pin (str): The PIN associated with the gift card.
        card_code (str): The code associated with the gift card.
        expiration_date (date): The expiration date of the gift card.
        condition (str): The condition of the gift card (e.g., new, used).
        restrictions (str): Any restrictions associated with the gift card.
        uploaded_image (ImageField): An optional image of the gift card.
        price (Decimal): The price at which the gift card is being sold.
    """

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="giftcard_seller")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="giftcard_buyer", blank=True)
    slug = models.SlugField(max_length = 50, blank=True)
    card_type = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    card_pin = models.CharField(max_length=255)
    card_code = models.CharField(max_length=255)
    expiration_date = models.DateField(null=True, blank=True)
    condition = models.CharField(max_length=255)
    restrictions = models.TextField(blank=True)
    uploaded_image = models.ImageField(upload_to='giftcards/', default="defaults/gift-card.png", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Returns a string representation of the GiftCard instance.
        """
        return f'{self.card_type} - {self.card_number}'
    
    def save(self, *args, **kwargs):
        """Auto-generate fields if not provided."""
        if not self.slug:
            self.slug = f"{self.seller}-{self.card_type}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("giftcard:giftcard-details", args=[self.slug])
