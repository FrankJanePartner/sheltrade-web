from django.shortcuts import render
from .models import Legal

# Create your views here.
def terms_conditions(request):
    return render(request, 'lagal/terms_conditions.html')