from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from core.models import Notification
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

# Fetch all admin users to notify them of new messages
admin_users = User.objects.filter(is_superuser=True)


def contactus(request):
    """
    Renders the contact us page with the appropriate base template.
    If the user is authenticated, a different base template is used.
    """
    user = User.objects.all()
    
    # Determine base template based on authentication status
    if request.user.is_authenticated:
        base_template = "formBase.html"  # For logged-in users
    else:
        base_template = "core/base.html"  # For guests
    
    context = {
        "user": request.user,  # Pass the current user
        "base_template": base_template,
    }
    return render(request, 'core/contactus.html', context)


def sendContact(request):
    """
    Handles contact form submissions.
    - Captures the name, email, and message from POST request.
    - Saves the data to the Contact model.
    - Sends an email notification to all admin users.
    - Displays a success message and reloads the contact page.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('message')

        # Save contact message to the database
        contact = Contact.objects.create(
            name=name,
            email=email,
            content=content,
        )
        
        # Notify admin users via email
        subject = f'Alert!!! {name} sent a message.'
        message_body = f"""
            {name} has sent a new message. Log in to your dashboard to view it.
        """
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in admin_users]  # Email all admins
        send_mail(subject, message_body, sender_email, recipient_list, fail_silently=False)

        # Show success message on the UI
        messages.success(request, "Message sent successfully")
        return render(request, 'core/contactus.html')


def contact_detail(request, slug):
    """
    Displays the details of a specific contact message.
    - Retrieves the message by its slug.
    - Marks the message as read if it hasn't been viewed yet.
    """
    contact = get_object_or_404(Contact, slug=slug)
    
    # Mark the message as read when viewed
    if not contact.read:
        contact.mark_as_read()
    
    context = {'contact': contact}
    return render(request, 'core/contact_detail.html', context)
