from django.conf import settings
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE, default='S')
    account_number = models.CharField(max_length=10, default=generate_acct_number, unique=True,
                                      primary_key=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    pin = models.CharField(max_length=4, validators=[validate_pin], default=0000)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_number} - {self.account_type}"


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('CREDIT', 'CRE'),
        ('DEBIT', 'DEB'),
        ('TRANSFER', 'TRA'),
        ('WITHDRAW', 'WITH')
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
    transaction_status = models.CharField(max_length=1, choices=Transaction_STATUS, default='S')
    transaction_id = models.CharField(max_length=9, default=generate_acct_number)
