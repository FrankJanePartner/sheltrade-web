from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from sheltradeAdmin.models import CryptoWallet, TransactionCharge
from .utils import COINGECKOAPI
from .models import UserAddress
from core.models import Profile
from wallet.models import Transaction, Wallet
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json


coingecko_Api = COINGECKOAPI()

@login_required
def sellcrypto(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    charge = get_object_or_404(TransactionCharge, id=1)
    crypto_addresses = CryptoWallet.objects.all()
    currency = profile.preferredCurrency.lower() if profile else "ngn"
    charge = get_object_or_404(TransactionCharge, id=1)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        crypto = request.POST.get('cryptoType')

        # Validate numeric inputs
        try:
            price = float(request.POST.get('amount', 0))
            coinValue = float(request.POST.get('coinValue', 0))
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('crypto:sellcrypto')

        # Correct charge calculations
        charge_amount = float(charge.charge)
        amount = price - charge_amount
        userReceives = coinValue * (float(charge.charge) / 100)
        
        # Create Transaction
        if crypto_addresses.minimumDeposit <= coinValue:
            user_transaction = Transaction.objects.create(
                user=request.user,
                transaction_type=f'Sell {crypto}',
                amount=price,
                status="pending"
            )
            messages.success(request, f'{crypto} of {price} Sold successfully!')
            return redirect('core:dashboard')
        else:
            messages.error(request, "Amount too small.")
            return redirect('crypto:sellcrypto')


    crypto_data = json.dumps(
        list(crypto_addresses.values("cryptoName", "cryptoSymbol", "walletAddress")),
        cls=DjangoJSONEncoder
    )

    context = {
        "cryptoAddresses": crypto_addresses,
        "charge": charge,
        "currency_symbol": currency,
        "cryptoData": crypto_data
    }

    
    return render(request, 'crypto/sellcrypto.html', context)
    

@login_required
def buycrypto(request):
    user = request.user
    balance = Wallet.objects.get(user=user)
    profile = Profile.objects.filter(user=user).first()
    charge = get_object_or_404(TransactionCharge, id=1)
    cryptoAddresses = CryptoWallet.objects.all()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    if request.method == 'POST':
        address = request.POST.get('address')
        crypto = request.POST.get('cryptoType')

        # Validate numeric inputs
        try:
            price = float(request.POST.get('amount', 0))
            coinValue = float(request.POST.get('coinValue', 0))
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('crypto:buycrypto')

        # Correct charge calculations
        charge_amount = float(charge.charge)
        amount = price - charge_amount
        userReceives = coinValue * (float(charge.charge) / 100)


        # Create Transaction
        if balance > price:
            user_transaction = Transaction.objects.create(
                user=request.user,
                transaction_type=f'Buy {crypto}',
                amount=price,
                status="pending"
            )

            # Store User Address
            user_address, created = UserAddress.objects.get_or_create(
                user=request.user,
                coin=crypto,
                defaults={"address": address}
            )

            messages.success(request, f'{crypto} of {price} purchased successfully!')
            return redirect('core:dashboard')
        else:
            messages.error(request, f'insufficient fund')
            return redirect('crypto:buycrypto')


    return render(request, 'crypto/buycrypto.html', {"cryptoAddresses": cryptoAddresses, "charge": charge})

@login_required
def fetch_coin_price(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    
    coin = request.GET.get('cryptoType').lower()
    print(coin)
    # amount = request.GET.get('amount')
    if profile:
        currency = profile.preferredCurrency.lower()
    else:
        currency = "ngn"

    print(currency)
    
    if coin:
        price_data = coingecko_Api.getprice(coin, currency)
        print(price_data)
        
        if "error" in price_data:
            return JsonResponse({"error": price_data["error"]}, status=500)
        
        return JsonResponse({"price": price_data.get(coin.lower(), {}).get(currency, 0)})
        
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

