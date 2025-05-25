from .models import BankDetail, CryptoWallet, SheltradeTeam

def details(request):

    bankDetail = BankDetail.objects.all()
    cryptoWallet = CryptoWallet.objects.all()
    sheltradeTeam = SheltradeTeam.objects.all()
    
    context = {
        'bankDetail':bankDetail,
        "cryptoWallet": cryptoWallet,
        "sheltradeTeam": sheltradeTeam
    }
    return context
