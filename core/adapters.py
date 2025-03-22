from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.models import Site
from django.http import JsonResponse
from django.shortcuts import redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """Allow signup for both API and web users."""
        return True

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """Send different confirmation emails for API and web users."""
        user = emailconfirmation.email_address.user
        current_site = Site.objects.get_current()
        site_domain = current_site.domain

        if request.path.startswith("/api/"):  # API users
            confirmation_url = f"https://{site_domain}/api/auth/verify-email/{emailconfirmation.key}/"
        else:  # Web users
            confirmation_url = f"https://{site_domain}/accounts/confirm-email/{emailconfirmation.key}/"

        ctx = {
            "user": user,
            "activate_url": confirmation_url,
            "request": request,
        }
        self.send_mail("account/email/email_confirmation", emailconfirmation.email_address.email, ctx)
        print(confirmation_url)

    def get_email_verification_redirect_url(self, request, email_address):
        """Handle email confirmation redirect differently for API and web users."""
        if request.path.startswith("/api/"):
            return JsonResponse({'detail': 'Account verification email has been sent.'})
        return redirect("account_email_verification_sent").url

    # def get_template_names(self, request,)
