from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Notification, Legal
from .utils import ExchangeRate
from wallet.models import Transaction, Wallet
from django.contrib import messages
from giftcard.models import GiftCard
from decimal import Decimal
from django.contrib.auth import authenticate, login

# Initialize the exchange rate utility
exchange = ExchangeRate()

def remove_first_char(s):
    """
    Removes the first character from a string if its length is greater than 10.
    
    Args:
        s (str): The input string.
    
    Returns:
        str: The modified string without the first character if applicable.
    """
    return s[1:] if len(s) > 10 else s

# Home page view
def home(request):
    """
    Renders the home page.
    """
    return render(request, 'core/home.html')

# About Us page view
def aboutus(request):
    """
    Renders the About Us page.
    """
    return render(request, 'core/aboutus.html')

@login_required
def dashboard(request):
    """
    Displays the user dashboard with transactions, notifications, and gift cards.
    Redirects workers to their dashboard if they belong to the 'Workers' group.
    """
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    giftcards = GiftCard.objects.filter(seller=user)
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()

    context = {
        "user": user,
        "transactions": transactions,
        'notifications': notifications,
        'unread_count': unread_count
    }

    if user.groups.filter(name='Workers').exists() or user.is_superuser:
        return redirect('/admin/')
    
    return render(request, 'core/dashboard.html', context)

@login_required
def profile(request):
    """
    Displays the profile of the logged-in user.
    """
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'profile/profile.html', {"profile": profile})

def preferred_currency(request):
    """
    Allows users to set or update their preferred currency.
    Updates the wallet balance based on the new currency exchange rate.
    """
    if request.method == "POST":
        currency = request.POST.get("currency")  # Retrieve currency from POST data
        user = request.user
        
        profile = Profile.objects.get(user=user)
        old_currency = profile.preferredCurrency
        wallet = Wallet.objects.get(user=user)
        user_balance = wallet.balance
        
        # Convert balance to the new currency
        result = exchange.get_price(old_currency, currency)
        rate = Decimal(result['conversion_rate'])
        wallet.balance = user_balance * rate
        wallet.save()

        profile.preferredCurrency = currency
        profile.save()

        Notification.objects.create(
            user=user,
            title='Preferred Currency Updated',
            content="Your Preferred Currency has been updated successfully."
        )

        messages.success(request, 'Your Preferred Currency has been updated.')
        return redirect('core:profile')

@login_required
def notification(request):
    """
    Displays user notifications.
    """
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'core/notification.html', {'notifications': notifications, 'unread_count': unread_count})

@login_required
def notification_detail(request, slug):
    """
    Displays the details of a specific notification.
    Marks the notification as read if it was unread.
    """
    notification = get_object_or_404(Notification, slug=slug)
    if not notification.is_read:
        notification.mark_as_read()
    return render(request, 'core/notificationDetail.html', {'notification': notification})

@login_required
def mark_all_as_read(request):
    """
    Marks all notifications as read for the logged-in user.
    """
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('core:notification')
    
@login_required    
def settings(request):
    """
    Renders the settings page for the user.
    """
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'profile/settings.html', {"profile": profile})

def addPhoneNumber(request):
    """
    Allows users to set or update their phone number.
    """
    if request.method == "POST":
        phone = request.POST.get("phone_Number")
        countries = request.POST.get('countries')
        user = request.user

        phone = remove_first_char(phone) if len(phone) > 10 else phone
        full_phone_number = countries + phone

        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_Number = full_phone_number
        profile.save()

        Notification.objects.create(
            user=user,
            title='Phone Number Updated',
            content="Your Phone Number has been updated successfully."
        )

        messages.success(request, 'Phone Number has been updated.')
        return redirect('core:profile')

def phoneNumberLogin(request):
    """
    Allows users to log in using their phone number and password.
    """
    if request.method == "POST":
        phone_number = request.POST.get('login')
        countries = request.POST.get('countries')
        password = request.POST.get('password')
        tel = countries + phone_number

        try:
            profile = Profile.objects.get(phone_Number=tel)
            user = authenticate(request, username=profile.user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user.username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid phone number or password')
        except Profile.DoesNotExist:
            messages.error(request, 'Phone number not found. Please login with email or username.')

    return render(request, 'account/login_with_phone_number.html')


def changeUserName(request):
    """
    Allows users to change their username.
    """
    if request.method == 'POST':
        new_username = request.POST.get('username')
        user = request.user

        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('core:settings')
        else:
            user.username = new_username
            user.save()
            Notification.objects.create(
                user=user,
                title='Change Username',
                content="Username changed successfully!"
            )
            messages.success(request, 'Username changed successfully!')
            return redirect('core:settings')


def changeNames(request):
    """
    Allows users to change their Names.
    """
    if request.method == 'POST':
        fName = request.POST.get('first_name')
        lName = request.POST.get('last_name')
        user = request.user

        user.first_name = fName
        user.last_name = lName
        user.save()
        Notification.objects.create(
            user=user,
            title='Change Names',
            content="First name and Last name updated successfully!"
        )
        messages.success(request, 'First name and Last name updated successfully!')
        return redirect('core:settings')


def legal(request, slug):
    """
    Displays a legal page based on the slug.

    Args:
        request: HTTP request.
        slug (str): Slug identifier for the legal page.

    Returns:
        Rendered legal page with legal content context.
    """
    legal = Legal.objects.filter(slug=slug).first()
    context = {
        'legal': legal,
    }
    return render(request, 'core/legal.html', context)

# Additional comments added to core/views.py for comprehensive documentation

# End of core/views.py
