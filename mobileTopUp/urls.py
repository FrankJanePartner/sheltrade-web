from django.urls import path
from .views import buyairtime, buydata, fetch_data_plans

app_name = 'mobileTopUp'

urlpatterns = [
    path('', buyairtime, name='buyairtime'),
    path('buyData/', buydata, name='buydata'),
    path('fetch-data-plans/', fetch_data_plans, name='fetch_data_plans'),
]
