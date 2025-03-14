from .models import BankDetail, CryptoWallet

def details(request):

    bankDetail = BankDetail.objects.all()
    cryptoWallet = CryptoWallet.objects.all()
    
    context = {
        'bankDetail':bankDetail,
        "cryptoWallet": cryptoWallet,
    }
    return context
