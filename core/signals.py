from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile
from wallet.models import Wallet
from .middleware import RequestMiddleware


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    request = RequestMiddleware.get_request()

    if created:
        # Create a profile instance for the new user
        Profile.objects.get_or_create(user=instance)
        Wallet.objects.get_or_create(user=instance)

        if request and request.path.startswith("/admin/auth/user/add/"):
            instance.is_staff = True  # Ensure staff status
            instance.save(update_fields=["is_staff"])  # Save only is_staff to avoid overriding other fields
        
        # Assign user to appropriate group
        if instance.is_staff and not instance.is_superuser:
            worker_group, _ = Group.objects.get_or_create(name="Workers")
            instance.groups.add(worker_group)
        elif not instance.is_staff and not instance.is_superuser:
            customer_group, _ = Group.objects.get_or_create(name="Customers")
            instance.groups.add(customer_group)
