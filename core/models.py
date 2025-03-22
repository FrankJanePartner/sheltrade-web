from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferredCurrency = models.CharField(max_length=10, help_text=_("Accepted currency for this account. E.g.: USD, EUR, NGN"), default="NGN")
    phone_Number  = models.CharField(max_length = 150, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    slug = models.SlugField(max_length=20, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']  # Show newest notifications first

    def __str__(self):
        return f"{self.user}:  {self.title} - {'Read' if self.is_read else 'Unread'}"
    
    def get_absolute_url(self):
        return reverse('core:notification_detail', args=[self.slug])

    def mark_as_read(self):
        """Marks the notification as read and saves it."""
        if not self.is_read:
            self.is_read = True
            self.save()
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(f'{self.id}{self.title}')[:20]  # Limit slug length
        super().save(*args, **kwargs)
        