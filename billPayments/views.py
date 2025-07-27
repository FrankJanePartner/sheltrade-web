"""
Views for billPayments app: handle TV subscriptions, electricity payments, and related pages.
"""

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
from decimal import Decimal

# Initialize the VTUAPI with the necessary keys
vtu_api = VTUBILLSAPI(VT_EMAIL, VT_PASSWORD)

def remove_first_char(s):
    """
    Remove the first character from a string if its length is greater than 10.
    This is used to normalize phone numbers that may have a leading zero or country code.
    """
    return s[1:] if len(s) > 10 else s

@login_required
@require_http_methods(["GET"])
def get_tv_services(request):
    """
    Fetch available TV service providers.

    Args:
        request: HTTP GET request with 'serviceID' parameter.

    Returns:
        JsonResponse with service variations or error message.
    """
    service_id = request.GET.get('serviceID')
    if service_id:
        services = vtu_api.getServices(service_id)
        return JsonResponse(services, safe=False)
    return JsonResponse({'error': 'Service ID is required.'}, status=400)


@require_http_methods(["POST"])
def subscribe_tv(request):
    """
    Handle TV subscription: Verify and process payment based on subscription type.

    Steps:
    - Validate user balance and input data.
    - Verify smart card number.
    - Process subscription renewal or change.
    - Deduct amount from user wallet with cashback.
    - Create transaction record.
    - Send email and notification to user.
    - Redirect to dashboard on success.

    Args:
        request: HTTP POST request with subscription data.

    Returns:
        JsonResponse on error or redirect on success.
    """
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.balance

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    error_message = None

    data = request.POST
    service_id = data.get('service-provider')
    billers_code = data.get('card-number')
    variation_code = data.get('service-plan')
    subscription_type = data.get('subscription-type')
    phone = data.get('phone')
    amount = data.get('amount')
    amount = float(amount)

    if len(phone) > 10:
        phone = remove_first_char(phone)

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
            balance = balance.balance - Decimal(amount - cashBackRate)
            balance.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type="Paid Cable bills",
                amount=amount,
                status="Approved"
            )

            # Send email to user
            subject = f'Paid Cable bills.'
            messageContent = f"Hi, {user}, Your Payment for {service_id} was successful."
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
                content=f"Your Payment for {service_id} was successful."
            )
            messages.success(
                request,
                f"Paid Cable bills successfully! You have received a {cashBackObj}% CashBack"
            )
            return redirect('core:dashboard')  # URL name for success.html

@login_required
def subs(request):
    """
    Render the subscriptions page.

    Args:
        request: HTTP request.

    Returns:
        Rendered subscriptions page.
    """
    return render(request, 'billPayment/subscriptions.html')

@require_http_methods(["POST"])
def pay_electricity(request):
    """
    Handle electricity bill payment: Verify meter and process payment.

    Steps:
    - Validate user balance and input data.
    - Verify meter number.
    - Process payment for prepaid or postpaid meter.
    - Deduct amount from user wallet with cashback.
    - Create transaction record.
    - Send email and notification to user.
    - Redirect to dashboard on success.

    Args:
        request: HTTP POST request with payment data.

    Returns:
        JsonResponse on error or redirect on success.
    """
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.balance

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    error_message = None

    data = request.POST
    service_id = data.get('serviceID')  # Electricity provider
    meter_number = data.get('meter_number')
    meter_type = data.get('meter_type')  # Prepaid or Postpaid
    phone = data.get('phone')
    amount = data.get('amount')
    amount = float(amount)

    if len(phone) > 10:
        phone = remove_first_char(phone)

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
        # Send email to user
        subject = f'Paid Electricity bills.'
        messageContent = f"Hi, {user}, Your Payment for {service_id} was successful."
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
            title='Paid Electricity bills',
            content=f"Your Payment for {service_id} was successful."
        )
        messages.success(
            request,
            f"Paid Electricity bills successfully! You have received a {cashBackObj}% CashBack"
        )

        # On success, redirect to success page
        return redirect('core:dashboard')

@login_required
def bills(request):
    """Render the bills page."""
    return render(request, 'billPayment/bills.html')
