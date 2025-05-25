from django.db import models
from django.utils.translation import gettext_lazy as _

# Model representing bank details for transactions
class BankDetail(models.Model):
    """
    Stores bank details including bank name, account number, and account holder's name.
    This is used to define banking details for transactions involving fiat currency.
    """
    bank_name = models.CharField(max_length=100, help_text=_("Name of the bank."))
    account_number = models.CharField(max_length=20, help_text=_("Bank account number."))
    account_holder_name = models.CharField(max_length=500, help_text=_("Name of the account holder."))
    currency = models.CharField(
        max_length=10,
        help_text=_("Accepted currency for this account. E.g.: USD, EUR, NGN"),
    )

    class Meta:
        verbose_name = "Bank Detail"
        verbose_name_plural = "Bank Details"

    def __str__(self):
        return f"Bank Details: {self.bank_name} - {self.account_number}"


# Model representing a cryptocurrency wallet
class CryptoWallet(models.Model):
    """
    Stores cryptocurrency wallet details, including wallet address, name, and symbol.
    Used for managing crypto transactions on the platform.
    """
    cryptoName = models.CharField(max_length=255, help_text=_("Full name of the cryptocurrency. E.g.: Bitcoin"))
    walletAddress = models.CharField(max_length=255, help_text=_("Wallet address for receiving cryptocurrency."))
    cryptoSymbol = models.CharField(
        max_length=10, help_text=_("Short symbol of the cryptocurrency. E.g.: BTC, ETH, USDT")
    )
    minimumDeposit = models.DecimalField(
        max_digits=25,
        decimal_places=20,
        blank=True,
        null=True,
        help_text=_("Minimum deposit amount. E.g: 0.00100000 ETH"),
    )

    class Meta:
        verbose_name = "Crypto Wallet"
        verbose_name_plural = "Crypto Wallets"

    def __str__(self):
        return f"{self.cryptoName} ({self.cryptoSymbol}) Wallet"


# Model representing a transaction charge for financial operations
class TransactionCharge(models.Model):
    """
    Stores the transaction fee percentage applied to Giftcard and Crypto transactions.
    The charge is stored as a percentage value.
    """
    charge = models.PositiveIntegerField(
        help_text=_("Percentage (%) per transaction for Giftcard, Crypto transactions.")
    )

    class Meta:
        verbose_name = "Transaction Charge"
        verbose_name_plural = "Transaction Charges"

    def __str__(self):
        return f"Transaction Charge: {self.charge}%"


# Model representing cashback rewards for certain transactions
class CashBack(models.Model):
    """
    Defines cashback rewards for transactions related to Airtime, Data, Electricity bills, and Cable bills.
    The cashback percentage is stored as an integer value.
    """
    amount = models.PositiveIntegerField(
        help_text=_("Percentage (%) cashback for Airtime, Data, Electric bills, and Cable bills transactions.")
    )

    class Meta:
        verbose_name = "Cash Back"
        verbose_name_plural = "Cash Backs"

    def __str__(self):
        return f"Cash Back: {self.amount}% for Airtime, Data, Bills"



# Model representing Sheltrade Team profile
class SheltradeTeam(models.Model):
    full_name = models.CharField(max_length=500)
    job_description = models.CharField(max_length=700)
    image = models.ImageField(upload_to="Images/Team", default="defaults/gift-card.png")

    class Meta:
        verbose_name = "Sheltrade Team"
        verbose_name_plural = "Sheltrade Team"

    def __str__(self):
        return self.full_name