from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

# Create your models here.
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userBalance = models.DecimalField(max_digits=1000, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} - {self.userBalance}'

class TransactionStatus:
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proof_of_payment = models.FileField(upload_to="images/proof_of_payment", blank=True)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=TransactionStatus.PAYMENT_STATUS, default=TransactionStatus.PENDING)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.status} - {self.id}"



class DepositNarations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit')
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='deposit')
    narration = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.user.username} deposited {self.transaction_id.amount} using narration"

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal')
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='withdrawal')
    acount_name = models.CharField(max_length=50)
    acount_number = models.CharField(max_length=50)
    BankName = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested a withdrawal of {self.transaction_id.amount} to  {self.acount_name}"



class WithdrawalAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_accounts')
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)  # Corrected the field name
    bank_name = models.CharField(max_length=50)  # Changed to lowercase for consistency
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} account {self.id}"


