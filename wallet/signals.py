from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Transaction,  Wallet, Deposit, Withdrawal
from core.models import Profile, Notification
from sheltradeAdmin.models import CryptoWallet
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags




@receiver(post_save, sender=User)
def create_user_transaction(sender, instance, created, **kwargs):
    if created:
        # Create a Transaction instance for the new user
        Notification.objects.create(
            user=instance,
            title='Account Created',
            content=f"Your Account was create successfully. Please log in to you email to verify your account."
            )
          # Adjust the amount or any other fields as necessary



@receiver(post_save, sender=Deposit)
def handle_User_deposits(sender, instance, created, **kwargs):

    user = instance.user
    transaction = instance.transaction
    balance, created = Wallet.objects.get_or_create(user=user)

    if instance.status == 'Approved':
        if transaction.status != 'Approved':
            transaction.status = 'Approved'
            transaction.save()
            balance.balance += instance.amount
            balance.save()

            Notification.objects.create(
                user=user,
                title='Fund Deposit.',
                content=f"""
                    Hi, {user},
                    Your Deposit was successfull.
                """
            )
        

    elif instance.status == 'Rejected':
        transaction.status = 'Rejected'
        transaction.save()
        Notification.objects.create(
                user=user,
                title='Fund Deposit.',
                content=f"""
                    Hi, {user},
                    Your Deposit was Failed.
                """
            )

    else:
        pass

@receiver(post_save, sender=Withdrawal)
def handle_User_withdrawal(sender, instance, created, **kwargs):

    user = instance.user
    transaction = instance.transaction
    balance = Wallet.objects.get(user=user)

    if instance.status == 'Sent':
        if transaction.status != 'Sent':
            transaction.status = 'Sent'
            transaction.save()
            balance.balance -= instance.amount
            balance.save()
            
            Notification.objects.create(
                user=user,
                title='Fund Withdrawal.',
                content=f"""
                    Hi, {user},
                    Your Withdrawal was successfull.
                """
            )
        

    elif instance.status == 'Declined':
        transaction.status = 'Declined'
        transaction.save()

        Notification.objects.create(
            user=user,
            title='Fund Withdrawal.',
            content=f"""
                Hi, {user},
                Your Withdrawal was Declined.
            """
        )

    else:
        pass


# @receiver(post_save, sender=Transaction)
# def handle_User_transactions(sender, instance, created, **kwargs):

#     user = instance.user
#     # Handle Crypto Transactions
#     crypto = next(
#         (c.cryptoName for c in CryptoWallet.objects.all() if c.cryptoName in instance.transaction_type),
#         None
#     )
#     balance = Wallet.objects.get(user=user)
#     cryptoWallet = CryptoWallet.objects.all()
    
#     # Handle Crypto Transactions
#     crypto = next(
#         (c.cryptoName for c in CryptoWallet.objects.all() if c.cryptoName in instance.transaction_type),
#         None
#     )


#     if instance.status == 'Approved':
#         if crypto and instance.transaction_type.startswith(f"Sell {crypto}"):
#             balance.balance += instance.amount
#             # Send email to user
#             subject = f'Crypto Sold'
#             messageContent = f"""
#                     Hi, {user},
#                     {crypto} of {instance.amount} Sold successfully
#                 """
#             sender_email = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]
#             html_content = render_to_string("email.html", {"messageContent": messageContent})
#             text_content = strip_tags(html_content)
#             email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
#             email.attach_alternative(html_content, "text/html")
#             email.send()

                    
#             # Send notification
#             Notification.objects.create(
#                 user=user,
#                 title='Sell {crypto}.',
#                 content=f"""
#                     Hi, {user},
#                     Your Sells of {crypto} was successfull.
#                 """
#             )
#         elif crypto and instance.transaction_type.startswith(f"Buy {crypto}"):
#             balance.balance -= instance.amount
#             # Send email to user
#             subject = f'Buy {crypto}'
#             messageContent = f"""
#                      Hi, {user},
#                     Your purchase of {crypto} was successfull.
#                 """
#             sender_email = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]
#             html_content = render_to_string("email.html", {"messageContent": messageContent})
#             text_content = strip_tags(html_content)
#             email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
#             email.attach_alternative(html_content, "text/html")
#             email.send()

                    
#             # Send notification
#             Notification.objects.create(
#                 user=user,
#                 title='Buy {crypto}.',
#                 content=f"""
#                     Hi, {user},
#                     Your purchase of {crypto} was successfull.
#                 """
#             )
#         balance.save()
#         if instance.status == 'Approved':
#             if instance.transaction_type == 'Sell Giftcard':
#                 giftcardBuyer.gift_card.status = "listed"
#                 giftcardBuyer.gift_card.save()  # Save the updated gift card status
#             elif instance.transaction_type == 'Buy Giftcard':
#                 giftcardBuyer.gift_card.status = "Sold"
#                 for giftcardBuyer in giftcardBuyers:
#                     seller = giftcardBuyer.gift_card.seller
#                     sellerBalance = Wallet.objects.get(user=seller)
                
#                 giftcardBuyer.escrow_status = "Sold"
#                 sellerBalance.balance += instance.amount
#                 sellerBalance.save()
#                 # Send email to user
#                 subject = f'GiftCard added'
#                 messageContent = f"""
#                         Hi, {user},
#                         Your sells fo GiftCard was successfull.
#                     """
#                 sender_email = settings.EMAIL_HOST_USER
#                 recipient_list = [user.email]
#                 html_content = render_to_string("email.html", {"messageContent": messageContent})
#                 text_content = strip_tags(html_content)
#                 email = EmailMultiAlternatives(subject, text_content, sender_email, recipient_list)
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()

                        
#                 # Send notification
#                 Notification.objects.create(
#                     user=user,
#                     title='GiftCard added',
#                     content=f"""
#                         Hi, {user},
#                         Your sells fo GiftCard was successfull.
#                     """
#                 )
#                 transaction = Transaction(user=seller, transaction_type='Sell Giftcard', amount=instance.amount, status="Approved")
#                 transaction.save()
#             else:
#                 pass

#         elif instance.status == 'Rejected':
#             if instance.transaction_type == 'Buy Giftcard':
#                 giftcardBuyer.gift_card.status = "Sold"
#                 for giftcardBuyer in giftcardBuyers:
#                     seller = giftcardBuyer.gift_card.seller
#                     sellerBalance = Wallet.objects.get(user=seller)
                
#                 giftcardBuyer.escrow_status = "Sold"
#                 sellerBalance.balance += instance.amount
#                 sellerBalance.save()
#                 transaction = Transaction(user=seller, transaction_type='Sell Giftcard', amount=instance.amount, status="Approved")
#                 transaction.save()


