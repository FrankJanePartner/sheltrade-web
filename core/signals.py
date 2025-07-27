from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile
from wallet.models import Wallet
from .middleware import RequestMiddleware
from django.db.models.signals import post_migrate


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a Profile and Wallet for a new User.

    Also assigns the user to appropriate groups based on staff status and
    sets staff status if the user was created via the admin interface.

    Args:
        sender (Model): The model class sending the signal (User).
        instance (User): The actual instance being saved.
        created (bool): True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    request = RequestMiddleware.get_request()

    if created:
        # Create a profile instance for the new user
        Profile.objects.get_or_create(user=instance)
        # Create a wallet instance for the new user with default balance 0.00
        Wallet.objects.get_or_create(user=instance, defaults={'balance': 0.00})

        # If the user was created via the Django admin user add page, ensure staff status
        if request and request.path.startswith("/admin/auth/user/add/"):
            instance.is_staff = True  # Ensure staff status
            instance.save(update_fields=["is_staff"])  # Save only is_staff to avoid overriding other fields
        
        # Assign user to appropriate group based on staff and superuser status
        if instance.is_staff and not instance.is_superuser:
            worker_group, _ = Group.objects.get_or_create(name="Workers")
            instance.groups.add(worker_group)
        elif not instance.is_staff and not instance.is_superuser:
            customer_group, _ = Group.objects.get_or_create(name="Customers")
            instance.groups.add(customer_group)


@receiver(post_migrate)
def create_worker_group(sender, **kwargs):
    """
    Signal handler to create the 'Workers' group after migrations.

    Ensures that the 'Workers' group exists in the database.

    Args:
        sender (Model): The model class sending the signal.
        **kwargs: Additional keyword arguments.
    """
    Group.objects.get_or_create(name='Workers')
