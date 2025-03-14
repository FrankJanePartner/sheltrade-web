from django.contrib import admin
from .models import BankDetail, CryptoWallet, TransactionCharge, CashBack

# Register your models here.
admin.site.register(BankDetail)
admin.site.register(CryptoWallet)
admin.site.register(TransactionCharge)
admin.site.register(CashBack)
