from django.contrib import admin
from .models import Legal

# Register your models here.
@admin.register(Legal)
class LegalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}