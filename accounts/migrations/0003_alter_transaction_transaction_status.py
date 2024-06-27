# Generated by Django 5.0.6 on 2024-06-27 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_balance_alter_account_pin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('P', 'PENDING'), ('S', 'SUCCESSFUL'), ('F', 'FAILED')], default='S', max_length=1),
        ),
    ]
