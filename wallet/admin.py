from django.contrib import admin
from .models import Wallet, Transaction, DepositNarations, Withdrawal, WithdrawalAccount

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Withdrawal)
admin.site.register(Transaction)
admin.site.register(DepositNarations)
admin.site.register(WithdrawalAccount)