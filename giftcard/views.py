from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import GiftCard, BuyGiftCard
from wallet.models import Transaction, Wallet
from sheltradeAdmin.models import TransactionCharge
from core.models import Notification
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Get all admin users
admin_users = User.objects.filter(is_superuser=True)

@login_required
def buygiftcard(request):
    giftcards =  GiftCard.objects.filter(status='Listed for Sale')
    charge =  get_object_or_404(TransactionCharge, id=1)

    context = {
        "giftcards":giftcards,
        "charge":charge
    }
    return render(request, 'giftcard/buygiftcard.html', context)

@login_required
def sellgiftcard(request):
    charge =  get_object_or_404(TransactionCharge, id=1)

    context = {
        "charge":charge,
    }
    return render(request, 'giftcard/sellgiftcard.html', context)

@login_required
def market(request):
    user = request.user
    giftcards = GiftCard.objects.filter(seller=user)
    return render(request, 'giftcard/market.html', {"giftcards":giftcards})

@login_required
def add_gift_card(request):
    if request.method == 'POST':
        seller = request.user  # Assuming the user is logged in
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        card_pin = request.POST.get('card_pin')
        card_code = request.POST.get('card_code')
        expiration_date = request.POST.get('expiration_date')
        condition = request.POST.get('condition')
        restrictions = request.POST.get('restrictions')
        price = request.POST.get('price')

        uploaded_image = request.FILES.get('uploaded_image')
        if uploaded_image:
            fs = FileSystemStorage()
            uploaded_image = fs.save(uploaded_image.name, uploaded_image)

        if expiration_date:
            try:
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
            except ValueError:
                return render(request, 'add_gift_card.html', {
                    'error': "Invalid date format. Please use YYYY-MM-DD."
                })
        else:
            expiration_date = None  # Set to None if no date is provided

        # Create the GiftCard instance
        gift_card = GiftCard(
            seller=seller,
            card_type=card_type,
            card_number=card_number,
            card_pin=card_pin,
            card_code=card_code,
            expiration_date=expiration_date,
            condition=condition,
            restrictions=restrictions,
            uploaded_image=uploaded_image,
            price=price
        )
        amount= float(price) - 0.01
        gift_card.save()
        
        transaction = Transaction(user=request.user, transaction_type='Sell Giftcard', amount=amount, status="pending")
        transaction.save()

        # Send email to Buyer notification
        subject = f'Alert!!! New Giftcard Added.'
        message = f"""
                {seller} just listed a list a new gift card and is waiting for your Approval.
            """
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in admin_users]
        send_mail(subject, message, sender_email, recipient_list, fail_silently=False)



        # created a new notification
        notification = Notification.objects.create(
            user=request.user,
            title='GiftCard added',
            content="""
                Gift add has been added and is waiting approval.
                Approval of giftcard take up to 24 hours
            """
        )
        notification.save()

        # ScrapyData = scrape_gift_card_granny(card_type)
        # if ScrapyData:
        #     # Do something with the price info (e.g., update the GiftCard model)
        #     gift_card.price = ScrapyData  # If you want to update the price based on scraping
        #     gift_card.save()

        messages.success(request, f"GiftCard Successfully uploaded")
        return redirect('core:dashboard')

    return render(request, 'add_gift_card.html')


from django.db import transaction as db_transaction  # Rename the module to avoid conflicts

@login_required
def buy_gift_card(request):
    charge = get_object_or_404(TransactionCharge, id=1)

    if request.method == 'POST':
        selected_amount = request.POST.get('card-amount')
        giftcard_id = request.POST.get('giftcard-id')
        buyer = request.user

        if not selected_amount or not giftcard_id:
            messages.error(request, 'Amount and gift card are required.')
            return redirect('giftcard:buygiftcard')

        try:
            with db_transaction.atomic():  # Use the renamed module alias
                amount = Decimal(selected_amount)
                selected_giftcard = GiftCard.objects.select_for_update().get(id=giftcard_id)
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                total_cost = amount + Decimal(charge.charge)
                image = selected_giftcard.uploaded_image

                if wallet.userBalance < total_cost:
                    messages.error(request, 'Insufficient balance in your wallet.')
                    return redirect('giftcard:buygiftcard')

                # Deduct amount from wallet
                wallet.userBalance -= total_cost
                wallet.save()

                # Create gift card purchase record
                buygiftcard = BuyGiftCard(
                    buyer=request.user,
                    gift_card=selected_giftcard,
                    escrow_status='held'
                )
                buygiftcard.save()

                # Record the transaction
                user_transaction = Transaction(  # Renamed to avoid conflict
                    user=request.user,
                    transaction_type='Buy Giftcard',
                    amount=total_cost,
                    status="pending"
                )
                user_transaction.save()

                # Send email to seller
                subject = f' Alert!!! Giftcard Sold.'
                messageContent = f"""
                        Hi, {selected_giftcard.seller},
                        Your {selected_giftcard.card_type} giftcard has been sold. Fund has been added to your wallet. Log into your account to see more.
                        Thank you for using Shel-Trade.
                    """
                link = "market"
                sender_email = settings.EMAIL_HOST_USER
                recipient_list = [selected_giftcard.seller.email]
                html_content = render_to_string("email.html", {"messageContent": messageContent, "link": link})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
                email.attach_alternative(html_content, "text/html")
                email.send()

                # Create seller notification
                notification = Notification.objects.create(
                    user=selected_giftcard.seller,
                    title='GiftCard added',
                    content="""
                        Giftcard {selected_giftcard.card_type} was card_type successfully.
                        Funds has been added to your wallet.
                    """
                )

                # Send email to Buyer
                subject = f' Alert!!! Giftcard Sold.'
                messageContent = f"""
                        Hi, {buyer},
                        Your {selected_giftcard.card_type} giftcard Details
                        card_type = {selected_giftcard.card_type}
                        card_number = {selected_giftcard.card_number}
                        card_pin = {selected_giftcard.card_pin }
                        card_code = {selected_giftcard.card_code}
                        expiration_date = {selected_giftcard.expiration_date}
                        condition = {selected_giftcard.condition}
                        restrictions = {selected_giftcard.restrictions}
                        price ={selected_giftcard.price}
                    """
                image = {selected_giftcard.uploaded_imagecard_type.read()}
                sender_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]
                html_content = render_to_string("email.html", {"messageContent": messageContent, "image": image})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
                email.attach_alternative(html_content, "text/html")
                email.send()

                # Create Buyer notification
                notification = Notification.objects.create(
                    user=request.user,
                    title='GiftCard added',
                    content="""
                        Giftcard Bought successfully.
                        Detail of card has been sent to your email
                    """
                )
                notification.save()

                messages.success(
                    request, f'Gift card for {selected_giftcard.card_type} purchased successfully! Total: ${total_cost:.2f}'
                )
                return redirect('core:dashboard')

        except (ValueError, GiftCard.DoesNotExist, Wallet.DoesNotExist):
            messages.error(request, 'Invalid input or gift card selection.')
            return redirect('giftcard:buygiftcard')

    return redirect('core:dashboard')


@login_required
def scrape_gift_card_granny(card_type):
    # Prepare the search URL for Gift Card Granny
    url = f"https://www.giftcardgranny.com/{card_type.lower().replace(' ', '-')}/"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            return None  # Return None if the page cannot be accessed

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the price information (modify the selectors based on the actual HTML structure)
        price_elements = soup.find_all('div', class_='price')  # Adjust class name as necessary
        prices = []

        for price_element in price_elements:
            price_text = price_element.get_text(strip=True)
            prices.append(price_text)

        return prices  # Return the list of prices

    except Exception as e:
        print(f"Error while scraping: {e}")
        return None






# from django.shortcuts import render, redirect
# from .models import GiftCard
# from .utils import validate_gift_card
# from wallet.models import Transaction, Wallet
# from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required
# def sellgiftcard(request):
#     if request.method == 'POST':
#         card_number = request.POST.get('card_number')
#         card_pin = request.POST.get('card_pin')
#         amount = request.POST.get('amount')

#         # Validate gift card using Zendit API
#         validation_result = validate_gift_card(card_number, card_pin)
#         if validation_result.get('status') == 'valid':
#             # Save to database if valid
#             gift_card = GiftCard.objects.create(
#                 user=request.user,
#                 card_number=card_number,
#                 card_pin=card_pin,
#                 amount=amount,
#                 status='on the market'
#             )
#             return redirect('core:dashboard')
#         else:
#             return render(request, 'sellgiftcard.html', {'error': 'Invalid Gift Card'})

#     return render(request, 'sellgiftcard.html')



# @login_required
# def buygiftcard(request, gift_card_id):
#     gift_card = GiftCard.objects.get(id=gift_card_id)

#     # Re-validate the gift card using Zendit API before purchase
#     validation_result = validate_gift_card(gift_card.card_number, gift_card.card_pin)
#     if validation_result.get('status') != 'valid':
#         gift_card.status = 'invalid'
#         gift_card.save()
#         # Notify seller
#         # (Implement notification logic)
#         return render(request, 'buygiftcard.html', {'error': 'Gift card no longer valid'})

#     # Check buyer's wallet balance
#     wallet = Wallet.objects.get(user=request.user)
#     if wallet.balance < gift_card.amount:
#         return render(request, 'buygiftcard.html', {'error': 'Insufficient balance'})

#     # Process the transaction
#     wallet.balance -= gift_card.amount
#     wallet.save()

#     # Create transaction records for buyer and seller
#     Transaction.objects.create(user=request.user, transaction_type='Purchased Gift Card', transaction_price=gift_card.amount, status='approved')
#     seller_wallet = Wallet.objects.get(user=gift_card.user)
#     seller_wallet.balance += gift_card.amount  # Subtract any platform fees
#     seller_wallet.save()
#     Transaction.objects.create(user=gift_card.user, transaction_type='Sold Gift Card', transaction_price=gift_card.amount, status='approved')

#     # Update gift card status
#     gift_card.status = 'sold'
#     gift_card.save()

#     # Notify buyer and seller via email
#     # (Implement email sending logic)

#     return redirect('core:dashboard')
