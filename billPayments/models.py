from django.db import models
from django.contrib.auth.models import User

# Models for handling utility bill payments such as TV subscriptions and electricity payments.

class TVSubscription(models.Model):
    """
    Represents a TV subscription payment made by a user.
    
    Attributes:
        user (ForeignKey): Links the subscription to a specific user.
        provider (CharField): The TV service provider (DSTV, GOTV, Startimes).
        smart_card_number (CharField): The smart card number associated with the subscription.
        amount (DecimalField): The amount paid for the subscription.
        status (CharField): The current status of the payment (Pending, Successful, Failed).
        created_at (DateTimeField): The timestamp when the payment was created.
    """
    
    PROVIDERS = [
        ('DSTV', 'DSTV'),
        ('GOTV', 'GOTV'),
        ('Startimes', 'Startimes'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who made the subscription.")
    provider = models.CharField(max_length=20, choices=PROVIDERS, help_text="TV service provider.")
    smart_card_number = models.CharField(max_length=20, help_text="Smart card number for the TV subscription.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid for the subscription.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Current status of the payment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the payment was created.")

    class Meta:
        verbose_name = 'TV Subscription'
        verbose_name_plural = 'TV Subscriptions'

    def __str__(self):
        """String representation of the TV subscription instance."""
        return f"{self.provider} - {self.smart_card_number}"

class ElectricityPayment(models.Model):
    """
    Represents an electricity bill payment made by a user.
    
    Attributes:
        user (ForeignKey): Links the payment to a specific user.
        provider (CharField): The electricity provider (Ikeja Electric, Eko Disco, Abuja Disco).
        meter_number (CharField): The meter number associated with the payment.
        meter_type (CharField): Specifies whether the meter is prepaid or postpaid.
        amount (DecimalField): The amount paid for the electricity bill.
        status (CharField): The current status of the payment (Pending, Successful, Failed).
        created_at (DateTimeField): The timestamp when the payment was created.
    """
    
    PROVIDERS = [
        ('Ikeja Electric', 'Ikeja Electric'),
        ('Eko Disco', 'Eko Disco'),
        ('Abuja Disco', 'Abuja Disco'),
    ]

    METER_TYPES = [
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who made the payment.")
    provider = models.CharField(max_length=50, choices=PROVIDERS, help_text="Electricity service provider.")
    meter_number = models.CharField(max_length=20, help_text="Meter number for the electricity payment.")
    meter_type = models.CharField(max_length=10, choices=METER_TYPES, help_text="Type of meter (prepaid/postpaid).")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid for electricity.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Current status of the payment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the payment was created.")

    class Meta:
        verbose_name = "Electricity Payment"
        verbose_name_plural = "Electricity Payments"

    def __str__(self):
        """String representation of the electricity payment instance."""
        return f"{self.provider} - {self.meter_number}"
