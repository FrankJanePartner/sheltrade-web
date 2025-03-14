from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SavedTransactionInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length = 150)
    provider = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Saved Transaction Info'
        verbose_name_plural = 'Saved Transaction Infos'

    def __str__(self):
        return f"{self.User} - {self.phone_number}"
