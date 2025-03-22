# Generated by Django 5.1.2 on 2025-03-22 00:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billPayments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricitypayment',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount paid for electricity.', max_digits=10),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp of when the payment was created.'),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='meter_number',
            field=models.CharField(help_text='Meter number for the electricity payment.', max_length=20),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='meter_type',
            field=models.CharField(choices=[('prepaid', 'Prepaid'), ('postpaid', 'Postpaid')], help_text='Type of meter (prepaid/postpaid).', max_length=10),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='provider',
            field=models.CharField(choices=[('Ikeja Electric', 'Ikeja Electric'), ('Eko Disco', 'Eko Disco'), ('Abuja Disco', 'Abuja Disco')], help_text='Electricity service provider.', max_length=50),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', help_text='Current status of the payment.', max_length=20),
        ),
        migrations.AlterField(
            model_name='electricitypayment',
            name='user',
            field=models.ForeignKey(help_text='User who made the payment.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount paid for the subscription.', max_digits=10),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp of when the payment was created.'),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='provider',
            field=models.CharField(choices=[('DSTV', 'DSTV'), ('GOTV', 'GOTV'), ('Startimes', 'Startimes')], help_text='TV service provider.', max_length=20),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='smart_card_number',
            field=models.CharField(help_text='Smart card number for the TV subscription.', max_length=20),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', help_text='Current status of the payment.', max_length=20),
        ),
        migrations.AlterField(
            model_name='tvsubscription',
            name='user',
            field=models.ForeignKey(help_text='User who made the subscription.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
