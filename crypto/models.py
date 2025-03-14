from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']
        verbose_name = 'UserAddress'
        verbose_name_plural = 'UserAddresses'

    def __str__(self):
        return f'{self.user.username} - {self.coin} - {self.address} - {self.id}'