from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class BankDetail(models.Model):
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=500)
    currency = models.CharField(max_length=10, help_text=_("Accepted currency for this account. E.g.: USD, EUR, NGN"))

    class Meta:
        verbose_name = 'BankDetail'
        verbose_name_plural = 'BankDetails'

    def __str__(self):
        return f"Sheltrde Bank Details"
    
class CryptoWallet(models.Model):
    cryptoName = models.CharField(max_length=255)
    walletAddress = models.CharField(max_length=255)
    cryptoSymbol = models.CharField(max_length=10, help_text=_("E.g.: BTC, ETH, USDT"))
    minimumDeposit = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True, help_text=_("Minimum deposit amount. E.g: 0.00100000 ETH"))

    class Meta:
        verbose_name = 'CryptoWallet'
        verbose_name_plural = 'CryptoWallets'

    def __str__(self):
        return f"Sheltrade {self.cryptoName} {self.cryptoSymbol} Wallet Details"

class TransactionCharge(models.Model):
    charge = models.PositiveIntegerField(help_text=_("Percentage(%) per transaction for Giftcard, Crypto"))

    class Meta:
        verbose_name = 'Transaction Charge'
        verbose_name_plural = 'Transaction Charges'

    def __str__(self):
        return f"Transaction Charge for Giftcard, Crypto"


class CashBack(models.Model):
    amount = models.PositiveIntegerField(help_text=_("Percentage(%) per transaction for Airtime, Data, Electric bills, Cable bills"))

    class Meta:
        verbose_name = 'Cash Back'
        verbose_name_plural = 'Cash Backs'

    def __str__(self):
        return f"Cash Back for Airtime, Data, Electric bills, Cable bills%"