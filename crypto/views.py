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
    """
    Handles the selling of cryptocurrency by the user.

    This view allows users to sell their cryptocurrency by providing the amount and 
    selecting the cryptocurrency type. It calculates the transaction charge and creates 
    a transaction record if the sale is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the dashboard or renders the sellcrypto template.
    """
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    charge = get_object_or_404(TransactionCharge, id=1)
    crypto_addresses = CryptoWallet.objects.all()
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
    """
    Handles the purchasing of cryptocurrency by the user.

    This view allows users to buy cryptocurrency by providing the amount and 
    selecting the cryptocurrency type. It checks the user's wallet balance and 
    creates a transaction record if the purchase is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the dashboard or renders the buycrypto template.
    """
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
    """
    Fetches the current price of a specified cryptocurrency.

    This view retrieves the price of a cryptocurrency based on the user's preferred currency
    and returns it as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the price of the cryptocurrency or an error message.
    """
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    
    coin = request.GET.get('cryptoType').lower()
    if profile:
        currency = profile.preferredCurrency.lower()
    else:
        currency = "ngn"
    
    if coin:
        price_data = coingecko_Api.getprice(coin, currency)
        
        if "error" in price_data:
            return JsonResponse({"error": price_data["error"]}, status=500)
        
        return JsonResponse({"price": price_data.get(coin.lower(), {}).get(currency, 0)})
        
    return JsonResponse({"error": "Invalid request"}, status=400)
