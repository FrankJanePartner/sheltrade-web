from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Contact(models.Model):
    """
    Model representing a contact message sent through the platform.
    
    Attributes:
        name (str): The name of the sender.
        slug (str): A unique identifier generated from the name and ID.
        email (str): The email address of the sender.
        content (str): The message content sent by the user.
        read (bool): Status indicating if the message has been read.
        created_at (datetime): Timestamp indicating when the message was created.
    """

    name = models.CharField(max_length=250, help_text=_("Full name of the sender"))
    slug = models.SlugField(max_length=50, blank=True, help_text=_("Auto-generated unique identifier for URL usage"))
    email = models.EmailField(max_length=254, help_text=_("Email address of the sender"))
    content = models.TextField(help_text=_("Message content"))
    read = models.BooleanField(default=False, help_text=_("Indicates if the message has been read"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, help_text=_("Timestamp when the message was created"))

    class Meta:
        """
        Metadata for the Contact model.
        """
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ['-created_at']  # Orders messages by most recent first

    def get_absolute_url(self):
        """
        Returns the absolute URL for the contact detail page.
        
        Returns:
            str: URL for the contact detail view.
        """
        return reverse('contact:contact_detail', args=[self.slug])

    def mark_as_read(self):
        """
        Marks the message as read if it is currently unread and saves the change.
        """
        if not self.read:
            self.read = True
            self.save()
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto-generate a slug from the name and ID.
        """
        if not self.slug:
            slug = f"{self.name} {self.id}"
            self.slug = slugify(slug)[:50]  # Limits slug length to 50 characters
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the contact message.
        
        Returns:
            str: A formatted string indicating the sender's name and read status.
        """
        return f"{self.name} sent a message. Read: {self.read}"
        


class SheltradeSocialMedia(models.Model):
    social_name = models.CharField(max_length=50)
    social_url = models.URLField(max_length = 200)

    def __str__(self):
        return self.social_name
    class Meta:
        verbose_name = 'Sheltrade Social Media'
        verbose_name_plural = 'Sheltrade Social Medias'


class SheltradeContact(models.Model):
    contact_name = models.CharField(max_length=50, help_text=_("Thsi is for shltrade phone numbers and emails"))
    contact_url = models.CharField(max_length = 200)

    def __str__(self):
        return self.contact_name
    class Meta:
        verbose_name = 'Sheltrade Contact'
        verbose_name_plural = 'Sheltrade Contacts'
