# Generated by Django 5.1.2 on 2025-05-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_alter_sheltradecontact_contact_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1),
        ),
    ]
