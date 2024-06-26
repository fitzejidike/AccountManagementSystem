# Generated by Django 5.0.6 on 2024-06-26 14:45

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(max_length=4, validators=[accounts.validators.validate_pin]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
