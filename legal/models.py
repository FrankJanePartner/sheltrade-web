from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class Legal(models.Model):
    name = models.URLField()
    slug = models.SlugField(max_length=100)    
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Legal"
        ordering = ['-created_at']


