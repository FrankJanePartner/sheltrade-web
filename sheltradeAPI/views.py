# FROM DJANGO IMPORTE
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView
from django.contrib.sites.models import Site

# FROM DRF IMPORT
from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken


# FROM SHELTRADE API APP INPORT
from .serializer import (
    UserSerializer, TVSubscriptionSerializer, ElectricityPaymentSerializer, ContactSerializer, ProfileSerializer,
    NotificationSerializer, GiftCardSerializer, BuyGiftCardSerializer, WalletSerializer, TransactionSerializer,
    DepositNarrationSerializer, WithdrawalSerializer, WithdrawalAccountSerializer
)

# OTHER APPS MODELS
from billPayments.models import TVSubscription, ElectricityPayment
from contact.models import Contact
from core.models import Profile, Notification
from crypto.models import UserAddress
from giftcard.models import GiftCard, BuyGiftCard
from mobileTopUp.models import SavedTransactionInfo
from sheltradeAdmin.models import BankDetail, CryptoWallet, TransactionCharge, CashBack
from wallet.models import Wallet, Transaction, DepositNarration, Withdrawal, WithdrawalAccount

# from workers.models import
from billPayments.utils import VTUBILLSAPI, VT_EMAIL, VT_PASSWORD
from core.utils import ExchangeRate
from crypto.utils import COINGECKOAPI
from mobileTopUp.utils import VTUAPI, API_KEY, PUBLIC_KEY, SECRET_KEY
from wallet.utils import generate_narration


# FROM PYTHON LIBRARY IMPORT
from decimal import Decimal
from allauth.account import app_settings

# CONSTANT VARIABLES
admin_users = User.objects.filter(is_superuser=True)
coingecko_Api = COINGECKOAPI()
exchange = ExchangeRate()
vtu_api2 = VTUAPI(API_KEY, PUBLIC_KEY, SECRET_KEY)
vtu_api = VTUBILLSAPI(VT_EMAIL, VT_PASSWORD)

# from allauth.account.adapter import get_adapter


def remove_first_char(s):
    return s[1:] if len(s) > 10 else s


# GET USER API
class UserListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# BILLPAYMENT API
class GetTVServices(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serviceID = request.data.get('serviceID')

        if serviceID:
            try:
                services = self.vtu_api.getServices(serviceID)
                return Response(services, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'could not send'})
        else:
            return Response({'error': 'Service ID is required'}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeTV(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TVSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            profile = get_object_or_404(Profile, user=user)
            currency = profile.preferredCurrency.lower() if profile else "ngn"

            balance = get_object_or_404(Wallet, user=user)
            user_balance = balance.userBalance

            cash_back = get_object_or_404(CashBack, id=1)
            cash_back_rate = float(cash_back.amount) / 100

            tv = get_object_or_404(TVSubscription, user=user)

            data = serializer.validated_data
            amount = float(data['amount'])

            if amount <= 0:
                return Response({'error': 'Amount must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            if amount > user_balance:
                return Response({'error': f'Insufficient Balance! You have {currency}{user_balance:.2f} available.'}, status=status.HTTP_400_BAD_REQUEST)

            request_id = vtu_api.generate_request_id()
            verify_response = vtu_api.verifySCNumber(data['billers_code'], data['service_id'])

            if 'error' in verify_response:
                return Response({'error': verify_response['error']}, status=status.HTTP_400_BAD_REQUEST)

            response = vtu_api.renewPlan(
                request_id, data['service_id'], data['billers_code'], data['variation_code'], amount, data['phone'], data['subscription_type'], 1
            )

            balance.userBalance -= (amount - cash_back_rate)
            balance.save()

            Transaction.objects.create(
                user=user,
                transaction_type="Paid Cable bills",
                amount=amount,
                status="Approved"
            )

            service_id = data['service_id']
            billers_code = data["billers_code"]
            if service_id not in tv.provider:
                tv.objects.create(
                    user=user,
                    provider=service_id,
                    smart_card_number=billers_code,
                    amount=amount,
                )

            self.send_email(user, data['service_id'])
            Notification.objects.create(
                user=user,
                title='Paid Cable bills',
                content=f'Your payment for {data["service_id"]} was successful.'
            )

            return Response({'message': f'Paid Cable bills successfully! You have received a {cash_back.amount}% CashBack'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, user, service_id):
        subject = 'Paid Cable bills'
        message_content = f"Hi {user.username}, Your payment for {service_id} was successful."
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        html_content = render_to_string("email.html", {"messageContent": message_content})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()


class PayElectricity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ElectricityPaymentSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            profile = get_object_or_404(Profile, user=user)
            currency = profile.preferredCurrency.lower() if profile else "ngn"

            balance = get_object_or_404(Wallet, user=user)
            user_balance = balance.userBalance

            cash_back = get_object_or_404(CashBack, id=1)
            cash_back_rate = float(cash_back.amount) / 100

            elect = get_object_or_404(ElectricityPayment, user=user)

            data = serializer.validated_data
            amount = float(data['amount'])

            if amount <= 0:
                return Response({'error': 'Amount must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            if amount > user_balance:
                return Response({'error': f'Insufficient Balance! You have {currency}{user_balance:.2f} available.'}, status=status.HTTP_400_BAD_REQUEST)

            request_id = vtu_api.generate_request_id()
            verify_response = vtu_api.verifyMeter(data['meter_number'], data['service_id'], data['meter_type'])

            if 'error' in verify_response:
                return Response({'error': verify_response['error']}, status=status.HTTP_400_BAD_REQUEST)

            response = vtu_api.prepaidMeter(request_id, data['service_id'], data['meter_number'], "default", amount, data['phone'])

            balance.userBalance -= (amount - cash_back_rate)
            balance.save()

            Transaction.objects.create(
                user=user,
                transaction_type="Paid Electricity bills",
                amount=amount,
                status="Approved"
            )

            self.send_email(user, data['service_id'])
            Notification.objects.create(
                user=user,
                title='Paid Electricity bills',
                content=f'Your payment for {data["service_id"]} was successful.'
            )

            service_id = data["service_id"]
            billers_code = data["meter_number"]
            if service_id not in elect.provider:
                elect.objects.create(
                    user=user,
                    provider=service_id,
                    smart_card_number=billers_code,
                    amount=amount,
                )

            return Response({'message': f'Paid Electricity bills successfully! You have received a {cash_back.amount}% CashBack'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, user, service_id):
        subject = 'Paid Electricity bills'
        message_content = f"Hi {user.username}, Your payment for {service_id} was successful."
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        html_content = render_to_string("email.html", {"messageContent": message_content})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()


# CONTACT API
class ContactViewSet(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    # @action(detail=True, methods=['POST'])
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        content = request.data.get('message')

        contact = Contact.objects.create(
            name=name,
            email=email,
            content=content
        )

        subject = f'Alert!!! {name} sent a message.'
        email_content = f"""
            {name} sent a new message. Login to your dashboard to view.
        """
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in admin_users]
        send_mail(subject, email_content, sender_email, recipient_list, fail_silently=False)

        return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)

class ContactDetailSet(APIView):
    def get(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        if not contact.read:
            contact.mark_as_read()
        serializer = ContactSerializer(contact)
        return Response(serializer.data)


# CORE API
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class PreferredCurrencyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        currency = request.data.get("currency")
        user = request.user

        profile = Profile.objects.get(user=user)
        wallet = Wallet.objects.get(user=user)
        result = exchange.get_price(profile.preferredCurrency, currency)
        rate = Decimal(result['conversion_rate'])

        wallet.userBalance *= rate
        wallet.save()

        profile.preferredCurrency = currency
        profile.save()

        Notification.objects.create(
            user=user,
            title='Preferred Currency Updated',
            content="Your preferred currency has been updated successfully."
        )

        return Response({"message": "Preferred currency updated successfully."})

class PhoneNumberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get("phone_Number")  # Get phone_Number from POST data
        countries = request.data.get('countries')
        user = request.user
        if len(str(phone)) > 10:
            phone = remove_first_char(phone)
        else:
            phone = phone
        phone_Number = f"{countries}{phone}"

        presentUserProfile = Profile.objects.get(user=user)
        presentUserPhoneNumber = presentUserProfile.phone_Number

        notifications = Notification.objects.filter(user=request.user)

        profile = Profile.objects.filter(user=user).first()
        if not profile:
            # Create a Profile if it doesn't exist
            profile = Profile.objects.create(user=user, phone_Number=phone_Number)
            profile.save()

            Notification.objects.create(
                user=user,
                title="Phone Number Set",
                content="Your Phone Number Has been added successfully",
            )

            return Response({"message": "Phone Number Has been set."})
        else:
            # Update the Phone Number
            profile.phone_Number = phone_Number
            profile.save()

            Notification.objects.create(
                user=user,
                title="Phone Number Updated",
                content="Your Phone Number Has been Updated successfully",
            )

            return Response({"message": "Phone Number Has been Updated."})


class PhoneNumberLoginView(APIView):

    def post(self, request):
        phone = request.data.get('phone_number')
        password = request.data.get('password')

        try:
            # Get user by phone number
            user_profile = Profile.objects.get(phone_Number=phone)
            user = user_profile.user

            # Authenticate using username
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": f"Welcome {user.username}",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                })
            else:
                return Response({"detail": "Invalid phone number or password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Profile.DoesNotExist:
            return Response({"message": "Phone number not found. Please login with email or username"}, status=status.HTTP_404_NOT_FOUND)



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        notification = get_object_or_404(Notification, slug=self.kwargs['slug'])
        if not notification.is_read:
            notification.mark_as_read()
        return notification

class MarkAllAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read."})

class ChangeUsernameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_username = request.data.get('username')

        if User.objects.filter(username=new_username).exists():
            return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.username = new_username
        request.user.save()

        Notification.objects.create(
            user=request.user,
            title='Username Changed',
            content="Your username has been changed successfully."
        )

        return Response({"message": "Username changed successfully."})


# CRYPTO API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_crypto(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    charge = get_object_or_404(TransactionCharge, id=1)
    crypto_addresses = CryptoWallet.objects.all()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    address = request.data.get('address')
    crypto = request.data.get('cryptoType')

    try:
        price = float(request.data.get('amount', 0))
        coin_value = float(request.data.get('coinValue', 0))
    except ValueError:
        return Response({"error": "Invalid amount entered."}, status=status.HTTP_400_BAD_REQUEST)

    charge_amount = float(charge.charge)
    amount = price - charge_amount
    user_receives = coin_value * (float(charge.charge) / 100)

    if crypto_addresses.first().minimumDeposit <= coin_value:
        Transaction.objects.create(
            user=user,
            transaction_type=f'Sell {crypto}',
            amount=price,
            status="pending"
        )
        return Response({"message": f'{crypto} of {price} sold successfully!'}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Amount too small."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_crypto(request):
    user = request.user
    balance = Wallet.objects.get(user=user)
    profile = Profile.objects.filter(user=user).first()
    charge = get_object_or_404(TransactionCharge, id=1)

    address = request.data.get('address')
    crypto = request.data.get('cryptoType')

    try:
        price = float(request.data.get('amount', 0))
        coin_value = float(request.data.get('coinValue', 0))
    except ValueError:
        return Response({"error": "Invalid amount entered."}, status=status.HTTP_400_BAD_REQUEST)

    charge_amount = float(charge.charge)
    amount = price - charge_amount
    user_receives = coin_value * (float(charge.charge) / 100)

    if balance.balance >= price:
        Transaction.objects.create(
            user=user,
            transaction_type=f'Buy {crypto}',
            amount=price,
            status="pending"
        )

        UserAddress.objects.get_or_create(
            user=user,
            coin=crypto,
            defaults={"address": address}
        )

        return Response({"message": f'{crypto} of {price} purchased successfully!'}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_coin_price(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    coin = request.query_params.get('cryptoType', '').lower()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    if coin:
        price_data = coingecko_Api.getprice(coin, currency)
        if "error" in price_data:
            return Response({"error": price_data["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"price": price_data.get(coin, {}).get(currency, 0)}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)


# GIFTCARD API
class GiftCardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        giftcards = GiftCard.objects.all()
        serializer = GiftCardSerializer(giftcards, many=True)
        return Response(serializer.data)

class GiftCardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            giftcard = GiftCard.objects.get(slug=slug)
            serializer = GiftCardSerializer(giftcard)
            return Response(serializer.data)
        except GiftCard.DoesNotExist:
            return Response({'error': 'Gift card not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateGiftCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiftCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateGiftCardView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, slug):
        try:
            giftcard = GiftCard.objects.get(slug=slug)
            if giftcard.user != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer = GiftCardSerializer(giftcard, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except GiftCard.DoesNotExist:
            return Response({'error': 'Gift card not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteGiftCardView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        try:
            giftcard = GiftCard.objects.get(slug=slug)
            if giftcard.user != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            giftcard.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GiftCard.DoesNotExist:
            return Response({'error': 'Gift card not found'}, status=status.HTTP_404_NOT_FOUND)


# MOBILETOPUP API
# Initialize the VTU API
def remove_first_char(s):
    return s[1:] if len(s) > 10 else s

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_airtime(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    balance = get_object_or_404(Wallet, user=user)
    user_balance = balance.userBalance

    cash_back_obj = get_object_or_404(CashBack, id=1)
    cash_back_rate = float(cash_back_obj.amount) / 100

    request_id = vtu_api.generate_request_id()

    network = request.data.get('network')
    phone_number = request.data.get('phone_number')
    amount = float(request.data.get('amount', 0))

    if len(phone_number) > 10:
        phone_number = remove_first_char(phone_number)

    if not network or not phone_number or amount <= 0:
        return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

    if amount > user_balance:
        return Response({'error': f'Insufficient Balance! You have {currency}{user_balance:.2f} available.'},
                        status=status.HTTP_400_BAD_REQUEST)

    buy_airtime_response = vtu_api2.buyairtime(request_id, network, amount, phone_number)

    if not buy_airtime_response or 'code' not in buy_airtime_response:
        return Response({'error': 'Invalid response from VTU API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if buy_airtime_response.get('code') == '000':
        balance.userBalance -= (amount - cash_back_rate)
        balance.save()
        Transaction.objects.create(user=user, transaction_type="Buy Airtime", amount=amount, status="Approved")

        send_mail(
            f'Buy Airtime',
            f'Hi {user}, your airtime of {currency}{amount} was successful.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        sti = SavedTransactionInfo.objects.all()

        if phone_number not in sti.phone_number:
            sti.objects.create(
                user=user,
                phone_number=phone_number,
                provider=network,
            )

        Notification.objects.create(user=user, title='Buy Airtime',
                                    content=f'Hi {user}, your airtime of {currency}{amount} was successful.')

        return Response({'message': f'{currency}{amount:.2f} {network} bought successfully!'}, status=status.HTTP_200_OK)

    return Response({'error': buy_airtime_response.get('response_description', 'Failed to purchase airtime.')},
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_data(request):
    user = request.user
    profile = Profile.objects.select_related("user").filter(user=user).first()
    currency = profile.preferredCurrency.lower() if profile else "ngn"

    balance = get_object_or_404(Wallet, user=user)
    user_balance = balance.userBalance

    cash_back_obj = get_object_or_404(CashBack, id=1)
    cash_back_rate = float(cash_back_obj.amount) / 100

    request_id = vtu_api.generate_request_id()

    service_id = request.data.get('serviceID')
    billers_code = request.data.get('billersCode')
    variation_code = request.data.get('variation_code')
    amount = float(request.data.get('amount', 0))
    phone = request.data.get('phone')
    sti = SavedTransactionInfo.objects.all()

    if len(phone) > 10:
        phone = remove_first_char(phone)

    if not service_id or not variation_code or not phone or amount <= 0:
        return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

    if amount > user_balance:
        return Response({'error': f'Insufficient Balance! You have {currency}{user_balance:.2f} available.'},
                        status=status.HTTP_400_BAD_REQUEST)

    buy_data_response = vtu_api2.buydata(request_id, service_id, billers_code, variation_code, amount, phone)

    if not buy_data_response or 'code' not in buy_data_response:
        return Response({'error': 'Invalid response from VTU API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if buy_data_response.get('code') == '000':
        balance.userBalance -= (amount - cash_back_rate)
        balance.save()
        Transaction.objects.create(user=user, transaction_type="Buy Data", amount=amount, status="Approved")

        send_mail(
            f'Buy Data',
            f'Hi {user}, your data plan of {variation_code} for {currency}{amount} was successful.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        if phone not in sti.phone_number:
            sti.objects.create(
                user=user,
                phone_number=phone,
                provider=service_id,
            )

        Notification.objects.create(user=user, title='Buy Data',
                                    content=f'Hi {user}, your data plan of {variation_code} for {currency}{amount} was successful.')

        return Response({'message': f'Data bought successfully!'}, status=status.HTTP_200_OK)

    return Response({'error': buy_data_response.get('response_description', 'Failed to purchase data.')},
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_data_plans(request):
    service_id = request.query_params.get('serviceID')

    if not service_id:
        return Response({'error': 'Invalid service ID.'}, status=status.HTTP_400_BAD_REQUEST)

    data_plans = vtu_api2.getDataPlan(service_id)
    plans = data_plans.get('content', {}).get('varations', [])

    if plans:
        return Response({'content': {'variations': plans}}, status=status.HTTP_200_OK)

    return Response({'error': 'No data plans available.'}, status=status.HTTP_404_NOT_FOUND)


# WALLET API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
        transactions = Transaction.objects.filter(user=user)
        data = {
            "wallet": {
                "balance": wallet.userBalance,
                "currency": wallet.currency,
            },
            "transactions": list(transactions.values())
        }
        return Response(data, status=status.HTTP_200_OK)
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    return Response(list(transactions.values()), status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit(request):
    narration = generate_narration()
    profile = Profile.objects.filter(user=request.user).first()
    data = {
        'narration': narration,
        'profile': profile.id if profile else None
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_submit_view(request):
    narration = request.data.get('narration')
    amount = Decimal(request.data.get('amount', 0))
    proof_of_payment = request.FILES.get('proof_of_payment')

    transaction = Transaction.objects.create(
        user=request.user,
        transaction_type='Deposit',
        proof_of_payment=proof_of_payment,
        amount=amount,
        status="pending"
    )

    DepositNarration.objects.create(user=request.user, narration=narration, transaction_id=transaction)

    admin_users = User.objects.filter(is_superuser=True)
    recipient_list = [user.email for user in admin_users]
    subject = 'Alert!!! New Deposit'
    message_content = {
        "Username": request.user.username,
        "Email": request.user.email,
        "Amount": amount,
        "Narration": narration
    }

    html_content = render_to_string("email.html", {"messageContent": message_content})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return Response({"message": "Deposit sent! Awaiting approval."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def withdrawal(request):
    withdrawal_accounts = WithdrawalAccount.objects.filter(user=request.user)
    return Response(list(withdrawal_accounts.values()), status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdrawal_submit_view(request):
    selected_account_id = request.data.get('SelectedAcount')
    amount = Decimal(request.data.get('amount'))

    try:
        withdrawal_account = WithdrawalAccount.objects.get(id=selected_account_id, user=request.user)
        wallet = Wallet.objects.get(user=request.user)

        if wallet.userBalance >= amount:
            transaction = Transaction.objects.create(user=request.user, transaction_type='Withdrawal', amount=amount, status="pending")
            Withdrawal.objects.create(
                user=request.user,
                transaction_id=transaction,
                acount_name=withdrawal_account.account_name,
                acount_number=withdrawal_account.account_number,
                BankName=withdrawal_account.bank_name
            )

            admin_users = User.objects.filter(is_superuser=True)
            recipient_list = [user.email for user in admin_users]
            subject = 'Alert!!! New Withdrawal'
            message_content = {
                "Username": request.user.username,
                "Email": request.user.email
            }

            html_content = render_to_string("email.html", {"messageContent": message_content})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": f"Withdrawal processed from {withdrawal_account.account_name}."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

    except WithdrawalAccount.DoesNotExist:
        return Response({"error": "Withdrawal account not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_account(request):
    account_name = request.data.get('accountName')
    bank_name = request.data.get('bankName')
    account_number = request.data.get('accountNumber')

    WithdrawalAccount.objects.create(user=request.user, account_name=account_name, account_number=account_number, bank_name=bank_name)

    Notification.objects.create(user=request.user, title='Added Account.', content="Account added successfully.")

    return Response({"message": "Account added successfully."}, status=status.HTTP_201_CREATED)


# WORKER API
