from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Wallet(models.Model):
    """
    Represents a user's wallet, storing their balance and cashback earned.

    This model tracks the user's wallet balance, cashback, and transaction history.

    Attributes:
        user (User): The user associated with this wallet.
        balance (Decimal): The current balance in the wallet.
        cashback (Decimal): The total cashback earned by the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    cashback = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        """
        Returns a string representation of the Wallet instance.
        """
        return f'{self.user.username} Wallet'

class Transaction(models.Model):
    """
    Represents a transaction made by the user.

    This model stores information about transactions, including the user, amount, 
    transaction type, and status.

    Attributes:
        user (User): The user associated with this transaction.
        transaction_type (str): The type of transaction (e.g., deposit, withdrawal).
        amount (Decimal): The amount involved in the transaction.
        status (str): The status of the transaction (e.g., completed, pending).
    """
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the Transaction instance.
        """
        return f'{self.transaction_type} Transaction by {self.user}  - {self.amount}'


class Deposit(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='deposit_transactions')
    naration = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    proof_of_payment = models.FileField(upload_to="proof_of_payment")
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')

    def __str__(self):
        return f'Deposit of {self.amount} by {self.user} -naration: {self.naration}'


class WithdrawalAccount(models.Model):
    """
    Represents a withdrawal account for the user.

    This model stores information about the user's withdrawal accounts.

    Attributes:
        user (User): The user associated with this withdrawal account.
        account_number (str): The account number for withdrawals.
        bank_name (str): The name of the bank associated with the account.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns a string representation of the WithdrawalAccount instance.
        """
        return f'{self.user.username} - {self.bank_name} - {self.account_number}'
    
    class Meta:
        verbose_name = 'WithdrawalAccount'
        verbose_name_plural = 'WithdrawalAccounts'


class Withdrawal(models.Model):
    """
    Represents a withdrawal made by the user.

    This model stores information about withdrawals, including the user, amount, 
    and status.

    Attributes:
        user (User): The user associated with this withdrawal.
        amount (Decimal): The amount withdrawn.
        status (str): The status of the withdrawal (e.g., completed, pending).
    """
    
    
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Declined', 'Declined'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='withdrawal_transactions')
    withdrawalAccount = models.ForeignKey(WithdrawalAccount, on_delete=models.CASCADE, related_name='withdrawal_Account')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')

    def __str__(self):
        """
        Returns a string representation of the Withdrawal instance.
        """
        return f'Withdrawal request of {self.amount} by {self.user}'
        
