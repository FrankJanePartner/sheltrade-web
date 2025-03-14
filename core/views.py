from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Notification
from .utils import ExchangeRate
from wallet.models import Transaction, Wallet
from django.contrib import messages
from giftcard.models import GiftCard
from decimal import Decimal
from django.contrib.auth import authenticate, login


exchange = ExchangeRate()


def remove_first_char(s):
    return s[1:] if len(s) > 10 else s


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def aboutus(request):
    return render(request, 'core/aboutus.html')

@login_required
def dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    giftcards = GiftCard.objects.filter(seller=user)
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()

    context = {
        "user":user,
        "transactions":transactions,
        'notifications': notifications,
        'unread_count': unread_count
        }

    worker_context = {
        "user":user,
        "transactions":transactions,
        'notifications': notifications,
        'unread_count': unread_count
        }

    if request.user.groups.filter(name='Workers').exists():
        return redirect('workers:dashboard', worker_context)
    return render(request, 'core/dashboard.html', context)

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'profile/profile.html', {"profile":profile})

@login_required
def preferred_currency(request):
    if request.method == "POST":
        currency = request.POST.get("currency")  # Get currency from POST data
        user = request.user
        
        presentUserProfile = Profile.objects.get(user=user)
        presentUserCurrency = presentUserProfile.preferredCurrency

        
        wallet = Wallet.objects.get(user=user)
        userBalance = wallet.userBalance
        
        result = exchange.get_price(presentUserCurrency, currency)
        rate = Decimal(result['conversion_rate'])

        wallet.userBalance = userBalance * rate
        wallet.save()


        # Check if the Profile exists
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            # Create a Profile if it doesn't exist
            profile = Profile.objects.create(user=user, preferredCurrency=currency)
            profile.save()

            Notification.objects.create(
                user=user,
                title='Preferred Currency Set',
                content="Your Preferred Currency Has been set successfully"
            )


            messages.success(request, 'Your Preferred Currency Has been set.')
        else:
            # Update the preferred currency
            profile.preferredCurrency = currency
            profile.save()

            Notification.objects.create(
                user=user,
                title='Preferred Currency Updated',
                content="Your Preferred Currency Has been Updated successfully"
            )

            messages.success(request, 'Your Preferred Currency Has been Updated.')
        return redirect('core:profile')
        # Handle the deposit logic here using the narration

@login_required
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'core/notification.html', {'notifications': notifications, 'unread_count': unread_count})

@login_required
def notification_detail(request, slug):
    notification = get_object_or_404(Notification, slug=slug)
    # Mark as read when viewed
    if not notification.is_read:
        notification.mark_as_read()
    context = {'notification': notification}
    return render(request, 'core/notificationDetail.html', context)


@login_required
def mark_all_as_read(request):
    """Marks all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('core:notification')


def settings(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'profile/settings.html', {"profile":profile})


def addPhoneNumber(request):
    if request.method == "POST":
        phone = request.POST.get("phone_Number")  # Get phone_Number from POST data
        countries = request.POST.get('countries')
        user = request.user
        if len(phone) > 10:
            phone = remove_first_char(phone)
        else:
            phone = phone
        phone_Number = countries+phone

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
                title='Phone Number Set',
                content="Your Phone Number Has been set successfully"
            )

            messages.success(request, 'Phone Number Has been set.')
        else:
            # Update the Phone Number
            profile.phone_Number = phone_Number
            profile.save()

            Notification.objects.create(
                user=user,
                title='Phone Number Updated',
                content="Your Phone Number Has been Updated successfully"
            )

            messages.success(request, 'Phone Number Has been Updated.')
        return redirect('core:profile')


def phoneNumberLogin(request):
    if request.method == "POST":
        code = request.POST.get('login')  # Get phone_Number from POST data
        countries = request.POST.get('countries')
        password = request.POST.get('password')
        user = request.user
        tel = countries+code

        try:
            # Check if the phone number exists in the profile
            user_profile = Profile.objects.get(phone_Number=tel)
            user = user_profile.user  # Get the associated user

            # Authenticate using the username (Allauth expects username or email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user.username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid phone number or password')
        except Profile.DoesNotExist:
            messages.error(request, 'Phone number not found. Please login with email or username')

    return render(request, 'account/login_with_phone_number.html')


def changeUserName(request):
    if request.method == 'POST':
        newUser = request.POST.get('username')
        user = request.user

        if User.objects.filter(username=newUser).exists():
            messages.error(request, 'Username is taken')
            return redirect('core:settings')
        else:
            user.username = newUser
            user.save()
            Notification.objects.create(
                user=user,
                title='Change Username',
                content="Username changed successfully!"
            )
            messages.success(request, f'Username changed successfully!')
            return redirect('core:settings')
