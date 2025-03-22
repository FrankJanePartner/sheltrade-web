"""
Signals for handling automatic creation of utility bill records (TV subscription and electricity payments)
whenever a transaction related to these services is approved.

This module listens for the `post_save` signal on the `Transaction` model and creates
appropriate records for `TVSubscription` and `ElectricityPayment` models.

### Key Components:
- **Django Signals (`post_save`)**: Triggered when a `Transaction` instance is created or updated.
- **Middleware (`RequestMiddleware`)**: Attempts to retrieve the request object, allowing access to form data.
- **Models Used**:
  - `Transaction` (wallet.models): Represents a payment transaction.
  - `TVSubscription`: Stores details of paid cable bills.
  - `ElectricityPayment`: Stores details of paid electricity bills.
  - `Profile`, `Notification`: Included for potential future extensions.
- **Fallback Mechanism**: Uses request data if available; otherwise, falls back to model fields.

### Expected Behavior:
- When a `Transaction` is saved and marked as `Approved`:
  - If it's a cable TV bill payment, a `TVSubscription` record is created.
  - If it's an electricity bill payment, an `ElectricityPayment` record is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile, TVSubscription, ElectricityPayment, Notification
from wallet.models import Transaction
from .middleware import RequestMiddleware

@receiver(post_save, sender=Transaction)
def create_user_bills_or_tv_model(sender, instance, created, **kwargs):
    """
    Signal to automatically create records for TV subscriptions or electricity payments
    when a new `Transaction` is created and approved.

    Parameters:
        sender (Model): The model class sending the signal (`Transaction`).
        instance (Transaction): The actual transaction instance being saved.
        created (bool): Indicates if a new instance was created.
        **kwargs: Additional keyword arguments.
    """
    # Attempt to retrieve the request object from middleware
    request = RequestMiddleware.get_request()

    # Proceed only if the transaction is newly created and has been approved
    if created and instance.status == "Approved":
        # Extract data from request if available, else use an empty dictionary
        if request:
            data = request.POST
        else:
            data = {}  # Prevents potential AttributeErrors

        # Handle Cable TV bill payments
        if instance.transaction_type == "Paid Cable bills":
            billers_code = data.get('card-number', instance.billers_code)  # Smart card number
            amount = data.get('amount', instance.amount)  # Payment amount
            service_id = data.get('service-provider', instance.service_id)  # Cable provider

            # Create a new TV subscription record
            TVSubscription.objects.create(
                user=instance.user,
                provider=service_id,
                smart_card_number=billers_code,
                amount=amount,
            )

        # Handle Electricity bill payments
        elif instance.transaction_type == "Paid Electricity bills":
            service_id = data.get('serviceID', instance.service_id)  # Electricity provider
            meter_number = data.get('meter_number', instance.meter_number)  # Meter number
            meter_type = data.get('meter_type', instance.meter_type)  # Prepaid/Postpaid type
            amount = data.get('amount', instance.amount)  # Payment amount

            # Create a new electricity payment record
            ElectricityPayment.objects.create(
                user=instance.user,
                provider=service_id,
                plan=meter_type,
                smart_card_number=meter_number,
                amount=amount,
            )
