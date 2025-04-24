from django.urls import path
from .views import terms_conditions


app_name = "legal"
urlpatterns = [
    path('<slug:slug>', terms_conditions, name='terms_conditions'),
]