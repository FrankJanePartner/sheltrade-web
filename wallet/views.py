from django.shortcuts import render, redirect
from .utils import generate_narration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, Wallet, DepositNarration, WithdrawalAccount, Withdrawal
from sheltradeAdmin.models import BankDetail
from core.models import Profile, Notification
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
@login_required
def wallet(request):
    user = request.user
    wallet = Wallet.objects.get(user=user)
    transactions = Transaction.objects.filter(user=user)

    context = {
        "wallet":wallet,
        "transactions":transactions,
    }

    return render(request, 'wallet/wallet.html', context)

@login_required
def transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    return render(request, 'wallet/transactions.html', {"transactions":transactions})

@login_required
def deposit(request):
    user = request.user
    narration = generate_narration()
    profile = Profile.objects.filter(user=user).first()

    context = {
        'narration': narration,
        'profile':profile,
    }
    
    return render(request, 'wallet/deposite.html', context)

@login_required
def deposit_submit_view(request):
    if request.method == 'POST':
        narration = request.POST.get('narration')

        amount = Decimal(request.POST.get('amount') or 0)
        proof_of_payment = request.FILES.get('proof_of_payment')
        

        transaction = Transaction(user=request.user, transaction_type='Deposit', proof_of_payment=proof_of_payment, amount=amount, status="pending")
        transaction.save()
        deposit_naration = DepositNarration(user=request.user, narration=narration, transaction_id=transaction)
        deposit_naration.save()


        # Prepare the email content
        subject = 'Alert!!! New Deposit'
        messageContent  = (
            f"Username: {request.user.username}\n"
            f"User's Email: {request.user.email}\n"
            f"Deposit Amount: {amount}\n"
            f"Narration: {narration}\n"
            f"Proof Of Payment: Attached below."
        )
        sender_email = settings.DEFAULT_FROM_EMAIL
        admin_users = User.objects.filter(is_superuser=True)
        recipient_list = [user.email for user in admin_users]
        image = {proof_of_payment.read()}

        context = {"messageContent": messageContent, "image": image}
        html_content = render_to_string("email.html", context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
            
        # send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

        messages.info(request, 'Deposit sent! Awaiting approval.')
        return redirect('wallet:wallet')
        # Handle the deposit logic here using the narration

@login_required
def withdrawal(request):
    withdrawalAccounts = WithdrawalAccount.objects.filter(user=request.user)
    
    return render(request, 'wallet/withdraw.html', {"withdrawalAccounts":withdrawalAccounts})


@login_required
def withdrawal_submit_view(request):
    if request.method == 'POST':
        selected_account_id = request.POST.get('SelectedAcount')
        amount = Decimal(request.POST.get('amount'))
        withdrawal_account= WithdrawalAccount.objects.get(id=selected_account_id, user=request.user)
        wallet = Wallet.objects.get(user=request.user)

        if wallet.userBalance >= amount:
            transaction = Transaction(user=request.user, transaction_type='Withdrawal', amount=amount, status="pending")
            transaction.save()
            withdrawal = Withdrawal(user=request.user, transaction_id=transaction, acount_name=withdrawal_account.account_name, acount_number=withdrawal_account.account_number, BankName=withdrawal_account.bank_name)
            withdrawal.save()

            # Prepare the email content
            subject = 'Alert!!! New Withdrawal'
            messageContent = (
                f"Username: {request.user.username}\n"
                f"User's Email: {request.user.email}\n"
                f"User's Email: {request.user.email}\n"
                f"Proof Of Payment: Attached below."
            )

            sender_email = settings.DEFAULT_FROM_EMAIL
            admin_users = User.objects.filter(is_superuser=True)
            recipient_list = [user.email for user in admin_users]
            html_content = render_to_string("email.html", {"messageContent": messageContent})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            messages.success(request, f"Withdrawal processed from {withdrawal_account.account_name}.")
            return redirect('wallet:wallet')
            
        else:
            messages.info(request, 'Insufficient balance.')
        return redirect('wallet:withdraw')


@login_required
def AddAccount(request):
    if request.method == 'POST':
        user = request.user
        accountName = request.POST.get('accountName')
        bankName = request.POST.get('bankName')
        accountNumber = request.POST.get('accountNumber')

        address = WithdrawalAccount(user=request.user, account_name=accountName, account_number=accountNumber, bank_name=bankName)
        address.save()

        # Send notification
        Notification.objects.create(
            user=user,
            title='Added Account.',
            content="""
                Account added sucessfully.
            """
        )
        messages.info(request, 'Account added sucessfully.')
        return redirect('wallet:wallet')
    else:
        return render(request, 'wallet/AddWithdrawalAccount.html')
    


    