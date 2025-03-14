from django.urls import path
from .views import contactus, sendContact, contact_detail

app_name = 'contact'

urlpatterns = [
    path('', contactus, name='contact'),
    path('sendContact/', sendContact, name='sendContact'),
    path('contact_detail/', contact_detail, name='contact_detail')
]
