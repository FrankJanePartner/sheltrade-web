from django.db import models
from django.contrib.auth.models import User


class SavedTransactionInfo(models.Model):
    """
    Model to store frequently used transaction details for a user.
    
    This allows users to save details such as phone numbers and service providers 
    they frequently use for transactions, enabling faster processing in future transactions.
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        help_text="The user to whom this transaction info belongs."
    )
    phone_number = models.CharField(
        max_length=150, 
        help_text="The saved phone number associated with the transaction."
    )
    provider = models.CharField(
        max_length=20, 
        help_text="The service provider associated with this phone number (e.g., MTN, Glo, Airtel)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="The timestamp when this transaction info was saved."
    )

    class Meta:
        verbose_name = 'Saved Transaction Info'
        verbose_name_plural = 'Saved Transaction Infos'
        ordering = ['-created_at']  # Display the most recently saved transactions first

    def __str__(self):
        """
        Returns a string representation of the saved transaction info,
        displaying the user's username and their saved phone number.
        """
        return f"{self.user.username} - {self.phone_number}"
