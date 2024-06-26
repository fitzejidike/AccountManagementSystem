from django.db import models
from accounts.utility import generate_acct_number
from .validators import validate_pin


# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPE = [
        ('S', 'SAVINGS'),
        ('C', 'CURRENT'),
        ('D', 'DOM')
    ]

    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE, default='S')
    account_number = models.CharField(max_length=10, default=generate_acct_number, unique=True,
                                      primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pin = models.CharField(max_length=4, validators=[validate_pin])
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0, )


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('CREDIT', 'CRE'),
        ('DEBIT', 'DEB'),
        ('TRANSFER', 'TRA')
    ]
    Transaction_STATUS = [
        ('P', 'PENDING'),
        ('S', 'SUCCESSFUL'),
        ('F', 'FAILED')
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE, default='CREDIT')
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    transaction_status = models.CharField(max_length=1, choices=Transaction_STATUS, default='P')
    transaction_id = models.CharField(max_length=9, default=generate_acct_number)
