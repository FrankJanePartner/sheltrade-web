"""
Views for giftcard app: handle listing, buying, selling, updating, and deleting gift cards.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GiftCard
from wallet.models import Wallet
from datetime import datetime
from django.http import HttpResponseForbidden

@login_required
def list_gift_card(request):
    """
    Lists all gift cards with status 'listed'.

    Args:
        request: HTTP request.

    Returns:
        Rendered gift card list page with giftcards context.
    """
    giftcards = GiftCard.objects.filter(status='listed')
    return render(request, 'giftcard/giftcard_list.html', {'giftcards': giftcards})

@login_required
def buy_gift_card(request):
    """
    Allows users to buy a gift card.

    This view handles the process of purchasing a gift card. It checks the user's wallet balance
    and updates the gift card status if the purchase is successful.

    Args:
        request: HTTP request.

    Returns:
        Redirects to dashboard on success or renders buy gift card page.
    """
    user = request.user
    wallet = Wallet.objects.get(user=user)
    giftcards = GiftCard.objects.filter(status="Listed")
    if request.method == 'POST':
        gift_card_id = request.POST.get('giftcard-id')
        try:
            gift_card = GiftCard.objects.get(id=gift_card_id)
        except GiftCard.DoesNotExist:
            messages.error(request, 'The selected gift card does not exist.')
            return redirect('giftcard:buy_gift_card')

        if wallet.balance >= gift_card.price:
            # Update the gift card as sold and assign buyer and sold_at
            gift_card.buyer = user
            gift_card.sold_at = datetime.now()
            gift_card.status = 'Sold'
            gift_card.save()
            messages.success(request, f'You have successfully purchased {gift_card.card_type}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Insufficient balance to purchase this gift card.')
            return redirect('giftcard:buy_gift_card')

    return render(request, 'giftcard/buygiftcard.html', {'giftcards': giftcards})

@login_required
def sell_gift_card(request):
    """
    Allows users to sell a gift card.

    This view handles the process of selling a gift card. It creates a GiftCard record if the sale is successful.

    Args:
        request: HTTP request.

    Returns:
        Redirects to dashboard on success or renders sell gift card page.
    """
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        card_pin = request.POST.get('card_pin')
        expiration_date_str = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')
        image = request.FILES.get('uploaded_image')

        expiration_date = None
        if expiration_date_str:
            try:
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                return render(request, 'giftcard/sellgiftcard.html')

        # Create a GiftCard record
        GiftCard.objects.get_or_create(
            seller=request.user,
            card_type=card_type,
            card_pin=card_pin,
            expiration_date=expiration_date,
            condition=condition,
            restrictions=restrictions,
            price=price,
            uploaded_image=image
        )
        messages.success(request, 'Your gift card has been listed for sale!')
        return redirect('core:dashboard')

    return render(request, 'giftcard/sellgiftcard.html')

@login_required
def gift_card_details(request, slug):
    """
    Displays and allows updating of a gift card's details.

    Args:
        request: HTTP request.
        slug (str): Slug identifier for the gift card.

    Returns:
        Renders gift card details page or redirects after update.
    """
    giftcard = get_object_or_404(GiftCard, slug=slug)

    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        card_pin = request.POST.get('card_pin')
        expiration_date_str = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')
        image = request.FILES.get('uploaded_image')

        expiration_date = None
        if expiration_date_str:
            try:
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                return render(request, 'giftcard/sellgiftcard.html', {'giftcard': giftcard})

        # Update the existing gift card
        giftcard.card_type = card_type
        giftcard.card_pin = card_pin
        giftcard.expiration_date = expiration_date
        giftcard.condition = condition
        giftcard.restrictions = restrictions
        giftcard.price = price

        if image:
            giftcard.uploaded_image = image

        giftcard.save()
        messages.success(request, 'Your gift card has been updated')
        return redirect('/giftcard/')

    return render(request, 'giftcard/giftcard_details.html', {'giftcard': giftcard})

@login_required
def delete_gift_card(request, slug):
    """
    Allows the seller to delete their gift card.

    Args:
        request: HTTP request.
        slug (str): Slug identifier for the gift card.

    Returns:
        Redirects to dashboard after deletion or renders confirmation page.
    """
    giftcard = get_object_or_404(GiftCard, slug=slug)

    # Ensure only the seller can delete their card
    if giftcard.seller != request.user:
        return HttpResponseForbidden("You're not allowed to delete this gift card.")

    if request.method == 'POST':
        giftcard.delete()
        messages.success(request, 'Gift card deleted successfully.')
        return redirect('core:dashboard')  # Replace with the page you want to redirect to after deletion

    return render(request, 'giftcard/confirm_delete.html', {'giftcard': giftcard})
