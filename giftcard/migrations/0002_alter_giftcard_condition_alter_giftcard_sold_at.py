# Generated by Django 5.1.2 on 2025-05-30 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giftcard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='condition',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='sold_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
