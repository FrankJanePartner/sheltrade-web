from django.urls import path
from .views import bills, get_tv_services, subscribe_tv, subs, pay_electricity

app_name = "billPayments"

urlpatterns = [
    path('', bills, name='bills'),  # URL for the bills page
    path('get-services/', get_tv_services, name='get_tv_services'),  # URL to fetch available TV services
    path('subscribe/', subscribe_tv, name='subscribe_tv'),  # URL to handle TV subscription
    path('subs/', subs, name='subs'),  # URL for the subscriptions page
    path('pay-electricity/', pay_electricity, name='pay-electricity'),  # URL to handle electricity bill payment
]