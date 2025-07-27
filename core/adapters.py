"""
Custom account adapter for handling user signup and email confirmation behavior.

This module extends the DefaultAccountAdapter from django-allauth to customize
the signup process, confirmation email sending, and email verification redirect
behavior. It differentiates between API users and web users to provide appropriate
URLs and responses for each context.
"""

# Import the default account adapter from django-allauth to extend its functionality
from allauth.account.adapter import DefaultAccountAdapter

# Import Site model to get the current site domain for constructing URLs
from django.contrib.sites.models import Site

# Import JsonResponse to send JSON responses for API users
from django.http import JsonResponse

# Import redirect to redirect web users after email verification
from django.shortcuts import redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to override default behaviors for signup and email confirmation.

    This adapter allows signup for all users and customizes the confirmation email
    and redirect URLs based on whether the request comes from an API or web user.
    """

    def is_open_for_signup(self, request):
        """
        Determine if signup is allowed.

        This implementation allows signup for both API and web users unconditionally.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True to allow signup.
        """
        return True

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Send a confirmation email with a customized URL depending on user type.

        Constructs different confirmation URLs for API users and web users,
        then sends the confirmation email with the appropriate context.

        Args:
            request: The HTTP request object.
            emailconfirmation: The EmailConfirmation instance.
            signup: Boolean indicating if this is part of a signup process.
        """
        # Get the user associated with the email confirmation
        user = emailconfirmation.email_address.user

        # Get the current site domain to build absolute URLs
        current_site = Site.objects.get_current()
        site_domain = current_site.domain

        # Determine the confirmation URL based on request path prefix
        if request.path.startswith("/api/"):  # API users
            confirmation_url = f"https://{site_domain}/api/auth/verify-email/{emailconfirmation.key}/"
        else:  # Web users
            confirmation_url = f"https://{site_domain}/accounts/confirm-email/{emailconfirmation.key}/"

        # Context for the email template
        ctx = {
            "user": user,
            "activate_url": confirmation_url,
            "request": request,
        }

        # Send the confirmation email using the specified template and context
        self.send_mail("account/email/email_confirmation", emailconfirmation.email_address.email, ctx)

        # Print the confirmation URL to the console for debugging purposes
        print(confirmation_url)

    def get_email_verification_redirect_url(self, request):
        """
        Provide the redirect URL or response after email verification.

        For API users, return a JSON response indicating success.
        For web users, redirect to the standard email verification sent page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: A redirect or JSON response depending on user type.
        """
        if request.path.startswith("/api/"):
            # Return JSON response for API users
            return JsonResponse({'detail': 'Account verification email has been sent.'})
        # Redirect web users to the email verification sent page
        return redirect("account_email_verification_sent").url

    # The following method is commented out and can be implemented if needed
    # def get_template_names(self, request,)
