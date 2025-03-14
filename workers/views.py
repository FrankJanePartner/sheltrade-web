from django.shortcuts import render
from contact.models import Contact
from crypto.models import UserAddress
from wallet.models import Transaction, WithdrawalAccount 

# Create your views here.


def dashboard(request):
    transactions = Transaction.objects.filter(status='Pending')
    contact = Contact.objects.filter(read=False)
    userAddress = UserAddress.objects.filter(user=transactions.user)
    userAccount = WithdrawalAccount.objects.filter(user=transactions.user)

    context = {
        "contact": contact,
        "transactions": transactions,
        "userAddress": userAddress,
        "userAccount": userAccount,
    }
    return render(request, 'workers/dashboard.html', context)
