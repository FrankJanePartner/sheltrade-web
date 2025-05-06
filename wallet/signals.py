from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Transaction,  Wallet, Deposit
from core.models import Profile, Notification
from giftcard.models import GiftCard, BuyGiftCard
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



@receiver(post_save, sender=Transaction)
def handle_User_transactions(sender, instance, created, **kwargs):

    user = instance.user
    # Handle Crypto Transactions
    crypto = next(
        (c.cryptoName for c in CryptoWallet.objects.all() if c.cryptoName in instance.transaction_type),
        None
    )
    userBalance = Wallet.objects.get(user=user)
    cryptoWallet = CryptoWallet.objects.all()
    
    # Handle Crypto Transactions
    crypto = next(
        (c.cryptoName for c in CryptoWallet.objects.all() if c.cryptoName in instance.transaction_type),
        None
    )


    if instance.status == 'Approved':
        if instance.transaction_type == "Deposit":
            userBalance.userBalance += instance.amount
            userBalance.save()
            # Send email to user
            subject = f' Fund Deposit.'
            messageContent = f"""
                    Hi, {user},
                    Your Deposit was successfull.
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
                title='Fund Deposit.',
                content=f"""
                    Hi, {user},
                    Your Deposit was successfull.
                """
            )
        elif instance.transaction_type == 'Withdrawal':
            userBalance.userBalance -= instance.amount
            userBalance.save()
            # Send email to user
            subject = f'Fund Withdrawal.'
            messageContent = f"""
                     Hi, {user},
                    Your Withdrawal was successfull.
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
                title='Fund Withdrawal.',
                content=f"""
                    Hi, {user},
                    Your Withdrawal was successfull.
                """
            )
        elif crypto and instance.transaction_type.startswith(f"Sell {crypto}"):
            userBalance.userBalance += instance.amount
            # Send email to user
            subject = f'Crypto Sold'
            messageContent = f"""
                    Hi, {user},
                    {crypto} of {instance.amount} Sold successfully
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
                title='Sell {crypto}.',
                content=f"""
                    Hi, {user},
                    Your Sells of {crypto} was successfull.
                """
            )
        elif crypto and instance.transaction_type.startswith(f"Buy {crypto}"):
            userBalance.userBalance -= instance.amount
            # Send email to user
            subject = f'Buy {crypto}'
            messageContent = f"""
                     Hi, {user},
                    Your purchase of {crypto} was successfull.
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
                title='Buy {crypto}.',
                content=f"""
                    Hi, {user},
                    Your purchase of {crypto} was successfull.
                """
            )
        userBalance.save()

    # Get the related BuyGiftCard instances for the user
    giftcardBuyers = BuyGiftCard.objects.filter(buyer=user)

    # Check if there are any BuyGiftCard instances
    if not giftcardBuyers.exists():
        return  # Early exit if no BuyGiftCard records found

    for giftcardBuyer in giftcardBuyers:
        seller = giftcardBuyer.gift_card.seller
        sellerBalance = Wallet.objects.get(user=seller)
        

        # Proceed with the transaction logic based on instance.status and transaction_type
        if instance.status == 'Approved':
            if instance.transaction_type == 'Sell Giftcard':
                giftcardBuyer.gift_card.status = "listed"
                giftcardBuyer.gift_card.save()  # Save the updated gift card status
            elif instance.transaction_type == 'Buy Giftcard':
                giftcardBuyer.gift_card.status = "Sold"
                for giftcardBuyer in giftcardBuyers:
                    seller = giftcardBuyer.gift_card.seller
                    sellerBalance = Wallet.objects.get(user=seller)
                
                giftcardBuyer.escrow_status = "Sold"
                sellerBalance.userBalance += instance.amount
                sellerBalance.save()
                # Send email to user
                subject = f'GiftCard added'
                messageContent = f"""
                        Hi, {user},
                        Your sells fo GiftCard was successfull.
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
                    title='GiftCard added',
                    content=f"""
                        Hi, {user},
                        Your sells fo GiftCard was successfull.
                    """
                )
                transaction = Transaction(user=seller, transaction_type='Sell Giftcard', amount=instance.amount, status="Approved")
                transaction.save()
            else:
                pass

        elif instance.status == 'Rejected':
            if instance.transaction_type == 'Buy Giftcard':
                giftcardBuyer.gift_card.status = "Sold"
                for giftcardBuyer in giftcardBuyers:
                    seller = giftcardBuyer.gift_card.seller
                    sellerBalance = Wallet.objects.get(user=seller)
                
                giftcardBuyer.escrow_status = "Sold"
                sellerBalance.userBalance += instance.amount
                sellerBalance.save()
                transaction = Transaction(user=seller, transaction_type='Sell Giftcard', amount=instance.amount, status="Approved")
                transaction.save()





@receiver(post_save, sender=Deposit)
def handle_User_deposits(sender, instance, created, **kwargs):
    if instance.status == 'Approved':
        transaction = Transaction.objects.get(transaction=instance.transaction, status="Approved")
        transaction.save()
    
    elif instance.status == 'Rejected':
        transaction = Transaction.objects.get(transaction=instance.transaction, status="Rejected")
        transaction.save()



                