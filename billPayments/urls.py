from django.urls import path
from .views import bills, get_tv_services, subscribe_tv, subs, pay_electricity

app_name = "billPayments"

urlpatterns = [
    path('', bills, name='bills'),
    path('get-services/', get_tv_services, name='get_tv_services'),
    path('subscribe/', subscribe_tv, name='subscribe_tv'),
    path('subs/', subs, name='subs'),
    path('pay-electricity/', pay_electricity, name='pay-electricity'),
]

