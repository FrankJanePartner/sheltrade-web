from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import GiftCard
from .verification import GiftCardVerifier

@staff_member_required
def verify_giftcard(request, card_id):
    card = get_object_or_404(GiftCard, id=card_id)
    if GiftCardVerifier.verify(card):
        messages.success(request, f"Gift card {card.card_type} - {card.price} verified successfully!")
    else:
        messages.error(request, f"Failed to verify gift card {card.card_type} - {card.price}")
    return redirect('admin:giftcards_giftcard_changelist')
