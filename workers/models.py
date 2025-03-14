from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WorkersActivity(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    workersAction = models.CharField(max_length = 150, verbose_name='Workers Actions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Worker's Activity"
        verbose_name_plural = "Worker's Activities"
        ordering = ['-created_at']
    

    def __str__(self):
        return self.worker
