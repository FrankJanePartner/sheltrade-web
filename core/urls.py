from django.urls import path
from .views import home, aboutus,  dashboard, profile, preferred_currency, notification, settings, notification_detail, mark_all_as_read, phoneNumberLogin, addPhoneNumber, changeUserName, changeNames, legal

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('about/', aboutus, name='aboutus'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path("preferred_currency/", preferred_currency, name="preferred_currency"),
    path('notification/', notification, name='notification'),
    path('notification_detail/<slug:slug>', notification_detail, name='notification_detail'),
    path('notifications/read/all/', mark_all_as_read, name='mark_all_as_read'),
    path('settings/', settings, name='settings'),
    path('accounts/login/phone_Number/', phoneNumberLogin, name='phoneNumberLogin'),
    path('accounts/add/phone_Number/', addPhoneNumber, name='addPhoneNumber'),
    path('accounts/username/change/', changeUserName, name='changeUserName'),
    path('accounts/name/update/', changeNames, name='changeNames'),
    path('legal/<slug:slug>/', legal, name='legal'),
]
