from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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
    path('api/', include('sheltradeAPI.urls')),

    # third party url
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
