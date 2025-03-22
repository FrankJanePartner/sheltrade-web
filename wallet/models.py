from django.db import models
from django.contrib.auth.models import User

# Define constants for transaction status
class TransactionStatus:
    """
    Defines the possible statuses for a transaction.
    """
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

class Wallet(models.Model):
    """
    Represents a user's wallet, storing their balance and cashback earned.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userBalance = models.DecimalField(max_digits=1000, decimal_places=2, default=0, help_text="Current balance in the user's wallet.")
    cashBackEarned = models.DecimalField(max_digits=1000, decimal_places=2, default=0, help_text="Total cashback earned by the user.")

    def __str__(self):
        return f'{self.user.username} - Balance: {self.userBalance}'

class Transaction(models.Model):
    """
    Represents a financial transaction made by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proof_of_payment = models.FileField(upload_to="images/proof_of_payment", blank=True, help_text="Upload proof of payment if required.")
    transaction_type = models.CharField(max_length=50, help_text="Type of transaction, e.g., Deposit, Withdrawal, Purchase.")
    amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0, help_text="Transaction amount.")
    status = models.CharField(max_length=10, choices=TransactionStatus.PAYMENT_STATUS, default=TransactionStatus.PENDING, help_text="Current transaction status.")
    date_time = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the transaction was created.")

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.status}"

class DepositNarration(models.Model):
    """
    Stores additional details about a deposit transaction.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit_narrations')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='deposit_narrations')
    narration = models.CharField(max_length=50, help_text="Additional description or reference for the deposit.")

    class Meta:
        verbose_name = 'Deposit Narration'
        verbose_name_plural = 'Deposit Narrations'
    
    def __str__(self):
        return f"{self.user.username} - {self.narration}"

class Withdrawal(models.Model):
    """
    Represents a withdrawal request by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='withdrawals')
    account_name = models.CharField(max_length=50, help_text="Account holder's name.")
    account_number = models.CharField(max_length=50, help_text="Bank account number.")
    bank_name = models.CharField(max_length=50, help_text="Bank name.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of withdrawal request.")

    def __str__(self):
        return f"{self.user.username} requested {self.transaction.amount} withdrawal to {self.account_name}" 

class WithdrawalAccount(models.Model):
    """
    Stores the user's preferred bank account for withdrawals.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_accounts')
    account_name = models.CharField(max_length=50, help_text="Name on the bank account.")
    account_number = models.CharField(max_length=50, help_text="Bank account number.")
    bank_name = models.CharField(max_length=50, help_text="Bank name.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of account addition.")

    class Meta:
        verbose_name = 'Withdrawal Account'
        verbose_name_plural = 'Withdrawal Accounts'

    def __str__(self):
        return f"{self.user.username} - {self.bank_name} Account"
