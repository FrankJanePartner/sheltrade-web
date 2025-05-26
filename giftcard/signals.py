from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Notification
from .models import GiftCard
from wallet.models import Wallet, Transaction



@receiver(post_save, sender=GiftCard)
def handle_User_GiftCards(sender, instance, created, **kwargs):

    user = instance.user
    balance = Wallet.objects.get(user=user)

    if instance.status == 'Sold':
        Transaction.objects.create(
            user=user,
            transaction_type='GiftCard Sold', amount=instance.price, status="Sold"
        )
        balance.balance += instance.amount
        balance.save()

        Notification.objects.create(
            user=user,
            title='GiftCard Sold.',
            content=f"""
                Hi, {user},
                Your GiftCard was sold successfull.
            """
        )
    

    elif instance.status == 'Rejected':
        Notification.objects.create(
                user=user,
                title='Rejected GiftCard.',
                content=f"""
                    Hi, {user},
                    Your GiftCard was Rejected.
                """
            )

    else:
        pass
