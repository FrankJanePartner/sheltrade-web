from django.db import migrations

def create_default_cashback(apps, schema_editor):
    CashBack = apps.get_model('sheltradeAdmin', 'CashBack')
    if not CashBack.objects.filter(id=1).exists():
        CashBack.objects.create(id=1, amount=5.0)  # Default 5% cashback

class Migration(migrations.Migration):

    dependencies = [
        ('mobileTopUp', '0001_initial'),
        ('sheltradeAdmin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_cashback),
    ]
