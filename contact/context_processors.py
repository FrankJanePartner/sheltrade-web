
from django.contrib.auth.models import User
from contact.models import SheltradeSocialMedia, SheltradeContact


def base_template(request):
    user = User.objects.all()
    if request.user.is_authenticated:
        base_template = "formBase.html"  # For authenticated users
    else:
        base_template = "core/base.html"  # For unauthenticated users

    context = {
        "user": request.user,  # No need to fetch from the database
        "base_template": base_template,
    }
    return context


def sheltrade_info(request):
    sheltradeSocialMedia = SheltradeSocialMedia.objects.all()
    sheltradeContact = SheltradeContact.objects.all()
    context = {
        "sheltradeSocialMedia" : sheltradeSocialMedia,
        "sheltradeContact" : sheltradeContact
    }
    return context
