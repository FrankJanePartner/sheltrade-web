from django.db import models
from django.contrib.auth.models import User

class UserAddress(models.Model):
    """
    Model representing a cryptocurrency wallet address associated with a user.

    This model stores cryptocurrency addresses linked to users, allowing them to 
    manage multiple wallet addresses for different coins.

    Attributes:
        user (User): The Django user associated with this wallet address.
        coin (str): The name of the cryptocurrency (e.g., Bitcoin, Ethereum).
        address (str): The actual wallet address where transactions can be sent.

    Meta:
        ordering (list): Orders entries by descending ID (newest first).
        verbose_name (str): A human-readable singular name for the model in Django Admin.
        verbose_name_plural (str): A human-readable plural name for the model in Django Admin.
    """

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="The user who owns this cryptocurrency address."
    )
    coin = models.CharField(
        max_length=255, 
        help_text="The name of the cryptocurrency (e.g., Bitcoin, Ethereum)."
    )
    address = models.CharField(
        max_length=255, 
        help_text="The wallet address associated with the specified cryptocurrency."
    )

    class Meta:
        ordering = ['-id']  # Orders records by newest first
        verbose_name = 'User Address'  # Display name in Django Admin (singular)
        verbose_name_plural = 'User Addresses'  # Display name in Django Admin (plural)

    def __str__(self):
        """
        Returns a human-readable string representation of the model instance.
        """
        return f'{self.user.username} - {self.coin} - {self.address} - {self.id}'
