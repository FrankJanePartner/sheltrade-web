from django.db import models
from core.models import Category, CommonInfo
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class VideoMessage(CommonInfo):
    link = models.CharField(max_length= 500, blank=True)
    images = models.FileField(upload_to="media/videoMessages")
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('sermons:videoStream', args=[self.slug])

    class Meta:
        verbose_name_plural = "VideoMessages"
        ordering = ['-uploaded_at']

class AudioMessage(CommonInfo):
    link = models.URLField()
    images = models.FileField(upload_to="media/AudioMessages")
    seriesDescription = HTMLField()
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('sermons:sermon_detail', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "AudioMessages"
        ordering = ['-uploaded_at']


