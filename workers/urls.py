from django.urls import path
from .views import dashboard


app_name = 'workers'

urlpatterns = [
    path('', dashboard, name='dashboard'),
]