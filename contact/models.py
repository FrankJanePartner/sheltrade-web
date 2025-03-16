from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50, blank=True)
    email = models.EmailField(max_length=254)
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('contact:contact_detail', args=[self.slug])

    def mark_as_read(self):
        if not self.read:
            self.read = True
            self.save()
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        slug = f"{self.name} {self.id}"
        if not self.slug:
            self.slug = slugify(slug)[:50]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} sent a message. Read: {self.read}"

