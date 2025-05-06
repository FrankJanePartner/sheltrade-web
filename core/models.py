from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField


# ============================
# User Profile Model
# ============================
class Profile(models.Model):
    """
    Represents a user profile linked to the Django built-in User model.
    Stores additional user information such as preferred currency and phone number.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        help_text=_("Links profile to a user account, deleting it if the user is removed.")
    )
    preferredCurrency = models.CharField(
        max_length=10, 
        help_text=_("Accepted currency for this account. E.g.: USD, EUR, NGN"), 
        default="NGN"
    )
    phone_Number = models.CharField(
        max_length=150, 
        blank=True, 
        null=True,
        help_text=_("User's phone number (optional).")
    )
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        """Returns a readable string representation of the profile."""
        return f"{self.user.username}'s Profile"


# ============================
# Notification Model
# ============================
class Notification(models.Model):
    """
    Represents notifications sent to users.
    Includes details such as title, content, timestamp, and read status.
    """
    user = models.ForeignKey(
        User, 
        related_name='notifications', 
        on_delete=models.CASCADE,
        help_text=_("User receiving the notification.")
    )
    title = models.CharField(
        max_length=150, 
        help_text=_("Title of the notification.")
    )
    slug = models.SlugField(
        max_length=20, 
        blank=True, 
        help_text=_("Unique slug generated from the title.")
    )
    content = models.TextField(help_text=_("Main message or content of the notification."))
    is_read = models.BooleanField(
        default=False, 
        help_text=_("Marks whether the notification has been read.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=True, 
        help_text=_("Timestamp when the notification was created.")
    )
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']  # Show newest notifications first
    
    def __str__(self):
        """Returns a readable string representation of the notification."""
        return f"{self.user}: {self.title} - {'Read' if self.is_read else 'Unread'}"
    
    def get_absolute_url(self):
        """Returns the absolute URL for a notification detail view."""
        return reverse('core:notification_detail', args=[self.slug])
    
    def mark_as_read(self):
        """Marks the notification as read and saves the change."""
        if not self.is_read:
            self.is_read = True
            self.save()
    
    def save(self, *args, **kwargs):
        """Automatically generates a slug from the title if not provided."""
        if not self.slug:
            self.slug = slugify(f'{self.id}{self.title}')[:20]  # Ensure slug length constraint
        super().save(*args, **kwargs)



# ============================
# Legal Model
# ============================
class Legal(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)    
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Legal"
        ordering = ['-created_at']


