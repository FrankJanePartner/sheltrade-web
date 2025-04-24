from django.shortcuts import render
from .models import Legal

# Create your views here.
def terms_conditions(request, slug):
    legal = Legal.objects.filter(slug=slug)
    context = {
        'legal':legal,
    }
    return render(request, 'lagal/terms_conditions.html', context)