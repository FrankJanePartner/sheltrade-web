from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile, Notification

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile instance for the new user
        Profile.objects.create(user=instance)

        # Assign user to the correct group
        if instance.is_staff and not instance.is_superuser:
            worker_group, _ = Group.objects.get_or_create(name='Workers')
            instance.groups.add(worker_group)
        elif not instance.is_staff and not instance.is_superuser:
            customer_group, _ = Group.objects.get_or_create(name='Customers')
            instance.groups.add(customer_group)
