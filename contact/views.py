from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from core.models import Notification
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


admin_users = User.objects.filter(is_superuser=True)

# Create your views here.
def contactus(request):
    user = User.objects.all()
    if request.user.is_authenticated:
        base_template = "formBase.html"  # For authenticated users
    else:
        base_template = "core/base.html"  # For unauthenticated users

    context = {
        "user": request.user,  # No need to fetch from the database
        "base_template": base_template,
    }
    return render(request, 'core/contactus.html', context)


def sendContact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('message')

        contact = Contact.objects.create(
            name=name,
            email=email,
            content=content,
        )
        
        # Send email to Buyer notification
        subject = f'Alert!!! {name} sent a message.'
        content = f"""
                {name} Send an new message. Login to you dashboard to view.
            """
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in admin_users]
        send_mail(subject, content, sender_email, recipient_list, fail_silently=False)

        messages.success(request, f"Message sent")
        return render(request, 'core/contactus.html')



def contact_detail(request, slug):
    contact = get_object_or_404(Contact, slug=slug)
    # Mark as read when viewed
    if not contact.is_read:
        contact.mark_as_read()
    context = {'contact': contact}
    return render(request, 'core/contact_detail.html', context)