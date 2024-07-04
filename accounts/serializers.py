from rest_framework import serializers

from accounts.models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'transaction_time', 'transaction_status', 'description']


class AccountSerializer(serializers.ModelSerializer):
    Transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'account_type']
        transactions = serializers.StringRelatedField(many=True)


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'pin', 'account_type']


class DepositWithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)


class WithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    pin = serializers.CharField(max_length=4)


class TransferSerializer(serializers.Serializer):
    sender_account = serializers.CharField(max_length=10)
    receiver_account = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class CheckBalanceSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    pin = serializers.CharField(max_length=4)