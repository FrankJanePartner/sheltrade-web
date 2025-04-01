from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact
from crypto.models import UserAddress
from wallet.models import Transaction, WithdrawalAccount
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def dashboard(request):
    transactions = Transaction.objects.filter(status='Pending')

    user_addresses = {}
    user_accounts = {}

    for transaction in transactions:
        user_addresses[transaction.user] = UserAddress.objects.filter(user=transaction.user).first()
        user_accounts[transaction.user] = WithdrawalAccount.objects.filter(user=transaction.user).first()

    contact = Contact.objects.filter(read=False)

    context = {
        "contact": contact,
        "transactions": transactions,
        "userAddresses": user_addresses,
        "userAccounts": user_accounts,
    }

    return render(request, 'workers/dashboard.html', context)

def transaactionDetails(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {
        "transaction": transaction,
    }
    return render(request, 'workers/transaction_details.html', context)
