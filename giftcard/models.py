from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class GiftCard(models.Model):
    """
    Model representing a gift card listed for sale by users.
    
    Attributes:
        seller (User): The user who is selling the gift card.
        card_type (str): The brand or retailer of the gift card (e.g., Amazon, Steam).
        card_number (str, optional): The unique number of the gift card.
        card_pin (str, optional): The PIN associated with the gift card.
        card_code (str, optional): Additional code if required for redemption.
        expiration_date (date, optional): The expiration date of the gift card.
        condition (str, optional): Condition of the gift card (new, used, or partially used).
        restrictions (str, optional): Any special conditions or usage restrictions.
        uploaded_image (ImageField, optional): An image of the gift card.
        price (Decimal): The price at which the seller is listing the gift card.
        status (str): The current status of the gift card (pending, invalid, listed, sold).
        created_at (datetime): The date and time when the gift card was created.
        updated_at (datetime): The date and time when the gift card was last updated.
    """
    
    # Choices for gift card statuses
    CARD_STATUSES = [
        ('pending', 'Pending Verification'),  # Awaiting admin validation
        ('invalid', 'Invalid'),  # Flagged as fake or incorrect
        ('listed', 'Listed for Sale'),  # Approved and available for buyers
        ('sold', 'Sold'),  # Purchased by a buyer
    ]

    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='cards', 
        null=True,
        help_text=_("The user who owns and is selling this gift card.")
    )
    card_type = models.CharField(
        max_length=50, 
        help_text=_("Brand/retailer name e.g., Amazon, Steam")
    )
    card_number = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        help_text=_("Unique number on the gift card (if applicable).")
    )
    card_pin = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        help_text=_("PIN code required for redemption (if applicable).")
    )
    card_code = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        help_text=_("Additional redemption code (if required).")
    )
    expiration_date = models.DateField(
        blank=True, 
        null=True, 
        help_text=_("Expiration date of the gift card, if applicable.")
    )
    condition = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        help_text=_("Condition of the gift card (e.g., new, used, partially used).")
    )
    restrictions = models.TextField(
        blank=True, 
        null=True, 
        help_text=_("Any specific terms or restrictions related to this card.")
    )
    uploaded_image = models.ImageField(
        upload_to='media/gift_cards/', 
        default="media/defaults/gift-card.png", 
        blank=True, 
        null=True,
        help_text=_("Optional: Image of the physical or digital gift card.")
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text=_("The price at which the seller lists this gift card.")
    )
    status = models.CharField(
        max_length=50, 
        choices=CARD_STATUSES, 
        default='pending', 
        db_index=True,
        help_text=_("Current status of the gift card (e.g., pending, invalid, listed, sold).")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text=_("Timestamp when the gift card was created.")
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text=_("Timestamp when the gift card details were last updated.")
    )

    def __str__(self):
        """
        String representation of the gift card model.
        """
        return f"{self.card_type} - {self.seller.username if self.seller else 'Unknown Seller'}"


class BuyGiftCard(models.Model):
    """
    Model representing a purchase transaction of a gift card.
    
    Attributes:
        buyer (User): The user who purchased the gift card.
        gift_card (GiftCard): The purchased gift card.
        escrow_status (str): The status of the escrow process (held, released, refunded).
        bought_at (datetime): The timestamp when the purchase occurred.
        updated_at (datetime): The timestamp of the last update to the transaction.
    """
    
    # Choices for escrow statuses
    ESCROW_STATUSES = [
        ('held', 'Held'),  # Payment is held in escrow
        ('released', 'Released'),  # Payment released to the seller
        ('refunded', 'Refunded')  # Payment refunded to the buyer
    ]

    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bought_cards', 
        null=True,
        help_text=_("The user who purchased the gift card.")
    )
    gift_card = models.ForeignKey(
        GiftCard, 
        on_delete=models.CASCADE, 
        related_name='bought', 
        null=True,
        help_text=_("Reference to the purchased gift card.")
    )
    escrow_status = models.CharField(
        max_length=10, 
        choices=ESCROW_STATUSES, 
        default='held',
        help_text=_("Current escrow status of the transaction (held, released, refunded).")
    )
    bought_at = models.DateTimeField(
        auto_now_add=True, 
        help_text=_("Timestamp when the gift card was purchased.")
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text=_("Timestamp when the transaction details were last updated.")
    )

    def __str__(self):
        """
        String representation of the BuyGiftCard model.
        """
        return f"{self.gift_card.card_type if self.gift_card else 'Unknown Gift Card'} bought by {self.buyer.username if self.buyer else 'Unknown Buyer'}"
