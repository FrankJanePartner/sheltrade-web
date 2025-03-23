from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from sheltradeAPI.views import CustomEmailVerificationSentView
# from allauth.account.views import email_verification_sent, ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView


admin.site.site_header = 'Sheltrade'
admin.site.site_title = 'Sheltrade Admin Panel'
admin.site.index_title = 'Sheltrade Administration'

urlpatterns = [
    path('admin/', admin.site.urls),

    # my apps url
    path('', include('core.urls', namespace='core')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('crypto/', include('crypto.urls', namespace='crypto')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('giftcard/', include('giftcard.urls', namespace='giftcard')),
    path('mobileTopUp/', include('mobileTopUp.urls', namespace='mobileTopUp')),
    path('billPayments/', include('billPayments.urls', namespace='billPayments')),
    path('workers/', include('workers.urls', namespace='workers')),
    # path('sheltradeAdmin/', include('sheltradeAdmin.urls', namespace='sheltradeAdmin')),
    path('api/', include('sheltradeAPI.urls', namespace='sheltradeAPI')),
    

    # third party url
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/', include('allauth.account.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# API URLs
urlpatterns += [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
