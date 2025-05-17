from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GiftCard, BuyGiftCard
from wallet.models import Wallet

@login_required
def buy_gift_card(request):
    """
    Allows users to buy a gift card.

    This view handles the process of purchasing a gift card. It checks the user's wallet balance
    and creates a BuyGiftCard record if the purchase is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the wallet or renders the buy gift card template.
    """
    user = request.user
    wallet = Wallet.objects.get(user=user)

    if request.method == 'POST':
        gift_card_id = request.POST.get('gift_card_id')
        gift_card = GiftCard.objects.get(id=gift_card_id)

        if wallet.userBalance >= gift_card.price:
            # Create a BuyGiftCard record
            BuyGiftCard.objects.create(buyer=user, gift_card=gift_card)
            messages.success(request, f'You have successfully purchased {gift_card.card_type}!')
            return redirect('wallet:wallet')
        else:
            messages.error(request, 'Insufficient balance to purchase this gift card.')
            return redirect('giftcard:buy_gift_card')

    gift_cards = GiftCard.objects.all()
    return render(request, 'giftcard/buy_gift_card.html', {'gift_cards': gift_cards})

@login_required
def gift_card_details(request):
    """
    Allows users to sell a gift card.

    This view handles the process of selling a gift card. It creates a GiftCard record if the sale is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the wallet or renders the sell gift card template.
    """
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        card_pin = request.POST.get('card_pin')
        card_code = request.POST.get('card_code')
        expiration_date = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')

        # Create a GiftCard record
        GiftCard.objects.create(
            seller=request.user,
            card_type=card_type,
            card_number=card_number,
            card_pin=card_pin,
            card_code=card_code,
            expiration_date=expiration_date,
            condition=condition,
            restrictions=restrictions,
            price=price
        )
        messages.success(request, 'Your gift card has been listed for sale!')
        return redirect('wallet:wallet')

    return render(request, 'giftcard/sell_gift_card.html')


@login_required
def sell_gift_card(request):
    """
    Allows users to sell a gift card.

    This view handles the process of selling a gift card. It creates a GiftCard record if the sale is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the wallet or renders the sell gift card template.
    """
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        card_pin = request.POST.get('card_pin')
        card_code = request.POST.get('card_code')
        expiration_date = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')

        # Create a GiftCard record
        GiftCard.objects.create(
            seller=request.user,
            card_type=card_type,
            card_number=card_number,
            card_pin=card_pin,
            card_code=card_code,
            expiration_date=expiration_date,
            condition=condition,
            restrictions=restrictions,
            price=price
        )
        messages.success(request, 'Your gift card has been listed for sale!')
        return redirect('wallet:wallet')

    return render(request, 'giftcard/sell_gift_card.html')



@login_required
def sell_gift_card(request):
    """
    Allows users to sell a gift card.

    This view handles the process of selling a gift card. It creates a GiftCard record if the sale is successful.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the wallet or renders the sell gift card template.
    """
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        card_pin = request.POST.get('card_pin')
        card_code = request.POST.get('card_code')
        expiration_date = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')

        # Create a GiftCard record
        GiftCard.objects.create(
            seller=request.user,
            card_type=card_type,
            card_number=card_number,
            card_pin=card_pin,
            card_code=card_code,
            expiration_date=expiration_date,
            condition=condition,
            restrictions=restrictions,
            price=price
        )
        messages.success(request, 'Your gift card has been listed for sale!')
        return redirect('wallet:wallet')

    return render(request, 'giftcard/sell_gift_card.html')