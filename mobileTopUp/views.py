from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .utils import VTUAPI, API_KEY, PUBLIC_KEY, SECRET_KEY
from wallet.models import Transaction, Wallet
from sheltradeAdmin.models import CashBack
from core.models import Profile, Notification
from django.core.mail import send_mail
from django.conf import settings

# Initialize the VTU API
vtu_api = VTUAPI(API_KEY, PUBLIC_KEY, SECRET_KEY)

def remove_first_char(s):
    return s[1:] if len(s) > 10 else s

@login_required
def buyairtime(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.userBalance

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    requestID = vtu_api.generate_request_id()
    error_message = None

    if request.method == 'POST':
        user = request.user
        network = request.POST.get('network')
        phone_number = request.POST.get('phone-number')
        amount = request.POST.get('amount')
        amount = float(amount)
        if len(phone_number) > 10:
            phone_number = remove_first_char(phone_number)
        else:
            phone_number = phone_number
            

        if not network:
            error_message = "Nework required."
        elif not phone_number:
            error_message = "Phone required."
        elif not amount:
            error_message = "Amount required."

        else:
            if amount <= 0:
                error_message = "Amount can not be less than or equal to zero."
            elif amount > userBalance:
                error_message = f"Insufficient Balance! You have {currency}{userBalance:.2f} available."
            else:
                buy_airtime_response = vtu_api.buyairtime(requestID, network, amount, phone_number)

                if "error" in buy_airtime_response:
                    return JsonResponse({'error': buy_airtime_response["error"]}, status=400)

                if not buy_airtime_response or "code" not in buy_airtime_response:
                    return JsonResponse({'error': "Invalid response from VTU API"}, status=500)

                if buy_airtime_response.get("code") == "000":  # Success response check
                    balance.userBalance -= (amount - cashBackRate)
                    balance.save()
                    Transaction.objects.create(
                        user=user,
                        transaction_type="Buy Airtime",
                        amount=amount,
                        status="Approved"
                    )
                    # Send email to user
                    subject = f'Buy Airtime.'
                    message = f"""
                            Hi, {user},
                            Your airtime of {currency}{amount} was successfull.
                        """
                    sender_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

                            
                    # Send notification
                    Notification.objects.create(
                        user=user,
                        title='Buy Airtime.',
                        content="""
                            Hi, {user},
                            Your airtime of {currency}{amount} was successfull.
                        """
                    )
                    messages.success(
                        request,
                        f"{currency}{amount:.2f} {network} bought successfully! You have recieve a {cashBackObj}% CashBack"
                    )
                    return redirect("core:dashboard")
                else:
                    error_message = buy_airtime_response.get("response_description", "Failed to purchase airtime.")
                    return JsonResponse({'error': error_message}, status=400)


    return render(request, 'mobileTopup/buyairtime.html', {'error': error_message})


@login_required
def buydata(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    # Fetch user's wallet and balance
    balance = get_object_or_404(Wallet, user=user)
    userBalance = balance.userBalance

    # Fetch cashback rate
    cashBackObj = get_object_or_404(CashBack, id=1)
    cashBackRate = float(cashBackObj.amount) / 100  # Convert percentage to float

    requestID = vtu_api.generate_request_id()
    error_message = None

    if request.method == 'POST':
        serviceID = request.POST.get('serviceID')
        billersCode = request.POST.get('billersCode')
        variation_code = request.POST.get('variation_code')
        amount = request.POST.get('amount')
        phone = request.POST.get('phone')
        amount = float(amount)
        if len(phone) > 10:
            phone = remove_first_char(phone)
        else:
            phone = phone

        if not serviceID or not variation_code or not phone:
            error_message = "All fields are required."
        else:
            if amount <= 0:
                error_message = "Amount can not be less than or equal to zero."
            elif amount > userBalance:
                error_message = f"Insufficient Balance! You have {currency}{userBalance:.2f} available."
            else:
                buy_data_response = vtu_api.buydata(requestID, serviceID, billersCode, variation_code, amount, phone)

                if "error" in buy_data_response:
                    return JsonResponse({'error': buy_data_response["error"]}, status=400)

                
                if not buy_data_response or "code" not in buy_data_response:
                    return JsonResponse({'error': "Invalid response from VTU API"}, status=500)


                if buy_data_response.get('code') == '000':  # Check for success
                    balance.userBalance -= (amount - cashBackRate)
                    balance.save()
                    Transaction.objects.create(
                        user=user,
                        transaction_type="Buy Data",
                        amount=amount,
                        status="Approved"
                    )
                    
                    # Send email to user
                    subject = f'Buy Data'
                    message = f"""
                            Hi, {user},
                            Your data plan of {variation_code } for {currency}{amount} was successfull.
                        """
                    sender_email = settings.EMAIL_HOST_USER
                    recipient_list = [settings.EMAIL_HOST_USER]
                    send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

                            
                    # Send notification
                    Notification.objects.create(
                        user=user,
                        title='Buy Data',
                        content="""
                                Hi, {user},
                                Your data plan of {variation_code } for {currency}{amount} was successfull.
                            """
                    )
                    messages.success(
                        request,
                        f"Data bought successfully! You have recieve a {cashBackObj}% CashBack"
                    )
                    return render(request, 'core:dashboard')
                else:
                    error_message = buy_data_response.get('response_description', 'Failed to purchase data.')

    return render(request, 'mobileTopup/buydata.html', {'error': error_message})


@login_required
def fetch_data_plans(request):
    service_id = request.GET.get('serviceID')
    
    if service_id:
        # Fetch the data plans from the API
        data_plans = vtu_api.getDataPlan(service_id)
        
        # Check for the correct key
        plans = data_plans.get('content', {}).get('varations') or []
        
        if plans:
            return JsonResponse({'content': {'variations': plans}}, status=200)  # Return the plans properly
        else:
            return JsonResponse({'error': 'No data plans available.'}, status=404)
    
    return JsonResponse({'error': 'Invalid service ID.'}, status=400)


