from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .utils import VTUBILLSAPI, VT_EMAIL, VT_PASSWORD
from .models import TVSubscription, ElectricityPayment
from wallet.models import Transaction, Wallet
from core.models import Profile, Notification
from sheltradeAdmin.models import CashBack
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Initialize the VTUAPI with the necessary keys
vtu_api =   VTUBILLSAPI(VT_EMAIL, VT_PASSWORD)

def remove_first_char(s):
    return s[1:] if len(s) > 10 else s

@login_required
@require_http_methods(["GET"])
def get_tv_services(request):
    """Fetch available TV service providers."""
    service_id = request.GET.get('serviceID')
    if service_id:
        services = vtu_api.getServices(service_id)
        return JsonResponse(services, safe=False)
    return JsonResponse({'error': 'Service ID is required.'}, status=400)


@login_required
@require_http_methods(["POST"])
def subscribe_tv(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.userBalance
    tv = get_object_or_404(TVSubscription, user=user)

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    error_message = None

    """Handle TV subscription: Verify and process payment based on subscription type."""
    data = request.POST
    service_id = data.get('service-provider')
    # service_id = data.get('serviceID')
    billers_code = data.get('card-number')
    variation_code = data.get('service-plan')
    subscription_type = data.get('subscription-type')
    phone = data.get('phone')
    amount = data.get('amount')
    amount = float(amount)

    if len(phone) > 10:
        phone = remove_first_char(phone)
    else:
        phone = phone

    # Generate a request ID
    request_id = vtu_api.generate_request_id()

    if amount <= 0:
        error_message = "Amount can not be less than or equal to zero."
    elif amount > userBalance:
        error_message = f"Insufficient Balance! You have {currency}{userBalance:.2f} available."
    else:
        # Step 1: Verify the smart card number
        verify_response = vtu_api.verifySCNumber(billers_code, service_id)

        if 'error' in verify_response:
            return JsonResponse({'error': verify_response['error']}, status=400)

        # Step 2: Check the subscription type and make the appropriate API call
        if subscription_type in ['renew', 'change']:
            return JsonResponse({'error': 'Invalid subscription type.'}, status=400)
        else:
            if subscription_type == "renew":
                response = vtu_api.renewPlan(
                    request_id, service_id, billers_code, variation_code, amount, phone, subscription_type, 1
                )
            elif subscription_type == "change":
                response = vtu_api.changePlan(
                    request_id, service_id, billers_code, variation_code, amount, phone, subscription_type, 1
                )
            balance.userBalance -= (amount - cashBackRate)
            balance.save()
            Transaction.objects.create(
                user=user,
                transaction_type="Paid Cable bills",
                amount=amount,
                status="Approved"
            )

            if service_id not in tv.provider:
                tv.objects.create(
                    user=user,
                    provider=service_id,
                    smart_card_number=billers_code,
                    amount=amount,
                )

            # Send email to user
            subject = f' Paid Cable bills.'
            messageContent = f"""
                    Hi, {user},
                    Your Payment for {service_id} was successfull.
                """
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            html_content = render_to_string("email.html", {"messageContent": messageContent})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Send notification
            Notification.objects.create(
                user=user,
                title='Paid Cable bills',
                content="""
                    Your Payment for {service_id} was successfull.
                """
            )
            messages.success(
                request,
                f"Paid Cable bills successfully! You have recieve a {cashBackObj}% CashBack"
            )
            return redirect('core:dashbord')  # URL name for success.html

@login_required
def subs(request):
    return render(request, 'billPayment/subscriptions.html')


@login_required
@require_http_methods(["POST"])
def pay_electricity(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.userBalance
    elect = get_object_or_404(ElectricityPayment, user=user)

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    error_message = None

    """Handle electricity bill payment: Verify meter and process payment."""
    data = request.POST
    service_id = data.get('serviceID')  # Electricity provider
    meter_number = data.get('meter_number')
    meter_type = data.get('meter_type')  # Prepaid or Postpaid
    phone = data.get('phone')
    amount = data.get('amount')
    amount = float(amount)

    if len(phone) > 10:
        phone = remove_first_char(phone)
    else:
        phone = phone

    # Generate request ID
    request_id = vtu_api.generate_request_id()

    if amount <= 0:
        error_message = "Amount can not be less than or equal to zero."
    elif amount > userBalance:
        error_message = f"Insufficient Balance! You have {currency}{userBalance:.2f} available."
    else:
        # Step 1: Verify meter number
        verify_response = vtu_api.verifyMeter(meter_number, service_id, meter_type)

        if 'error' in verify_response:
            return JsonResponse({'error': verify_response['error']}, status=400)

        # Step 2: Make payment based on meter type
        if meter_type in ['renew', 'change']:
            return JsonResponse({'error': 'Invalid meter type.'}, status=400)
        else:
            if meter_type == "prepaid":
                response = vtu_api.prepaidMeter(request_id, service_id, meter_number, "default", amount, phone)
            elif meter_type == "postpaid":
                response = vtu_api.postpaidMeter(request_id, service_id, meter_number, "default", amount, phone)

        # Check for payment errors
        if 'error' in response:
            return JsonResponse({'error': response['error']}, status=400)

        balance.userBalance -= (amount - cashBackRate)
        balance.save()
        Transaction.objects.create(
            user=user,
            transaction_type="Paid Electricity bills",
            amount=amount,
            status="Approved"
        )

        if service_id not in elect.provider:
            elect.objects.create(
                user=user,
                provider=service_id,
                plan=meter_type,
                smart_card_number=meter_number,
                amount=amount,
            )
        # Send email to user
        subject = f' Paid Cable bills.'
        messageContent = f"""
                Hi, {user},
                Your Payment for {service_id} was successfull.
            """
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        html_content = render_to_string("email.html", {"messageContent": messageContent})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()

        # Send notification
        Notification.objects.create(
            user=user,
            title='Paid Paid Electricity bills',
            content="""
                Your Payment for {service_id} was successfull.
            """
        )
        messages.success(
            request,
            f"Paid Electricity bills successfully! You have recieve a {cashBackObj}% CashBack"
        )

        # On success, redirect to success page
        return redirect('core:dashbord')

@login_required
def bills(request):
    return render(request, 'billPayment/bills.html')
