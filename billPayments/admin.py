from django.contrib import admin
from .models import TVSubscription, ElectricityPayment

# Create your models here.
admin.site.register(TVSubscription)
admin.site.register(ElectricityPayment)
