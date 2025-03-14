from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TVSubscription(models.Model):
    PROVIDERS = [
        ('DSTV', 'DSTV'),
        ('GOTV', 'GOTV'),
        ('Startimes', 'Startimes'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    smart_card_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'TV Subscription'
        verbose_name_plural = 'TV Subscriptions'


    def __str__(self):
        return f"{self.provider} - {self.smart_card_number}"

class ElectricityPayment(models.Model):
    PROVIDERS = [
        ('Ikeja Electric', 'Ikeja Electric'),
        ('Eko Disco', 'Eko Disco'),
        ('Abuja Disco', 'Abuja Disco'),
    ]

    METER_TYPES = [
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    meter_number = models.CharField(max_length=20)
    meter_type = models.CharField(max_length=10, choices=METER_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Electricity Payment"
        verbose_name_plural = "Electricity Payments"

    def __str__(self):
        return f"{self.provider} - {self.meter_number}"
