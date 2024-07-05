from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account, Transaction
from .serializers import AccountCreateSerializer, DepositWithdrawSerializer, WithdrawSerializer, \
    CheckBalanceSerializer, TransferSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer


# class ListAccount(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer
# 
# 
# class AccountDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer

# lookup_field = 'account_number'


# @api_view(['GET', 'POST'])
# def list_accounts(request):
#     if request.method == 'GET':
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = AccountCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#

# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def accounts_details(request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     if request.method == 'GET':
#         serializer = AccountSerializer(account)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PUT":
#         serializer = AccountCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PATCH":
#         serializer = AccountCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         account.delete()
#         return Response(status=status.HTTP_204_NO_CONT
class Deposit(APIView):
    def post(self, request):
        serializer = DepositWithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)
        balance = account.balance
        balance += amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount,

        )
        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'CRED'
        return Response(data=transaction_details, status=status.HTTP_200_OK)


class Withdraw(APIView):
    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        pin = serializer.data['pin']
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)
        balance = account.balance
        if balance >= amount:
            balance -= amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount,
            pin=pin,

        )
        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'WITH'
        return Response(data=transaction_details, status=status.HTTP_200_OK)


class CheckBalance(APIView):
    def GET(self, request):
        serializer = CheckBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        pin = serializer.data['pin']
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)


class TransferViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = TransferSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender_account = serializer.data['account_number']
        receiver_account = serializer.data['receiver_account_number']
        amount = Decimal(serializer.data['amount'])
        transaction_details = {}
        sender_account_from = get_object_or_404(Account, pk=sender_account)
        receiver_account_to = get_object_or_404(Account, pk=receiver_account)
        balance = sender_account_from.balance
        transaction_details = {}
        if balance > amount:
            balance -= amount
        else:
            return Response(data={"message": "insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transferred_balance = receiver_account_to.balance + amount
            Account.objects.filter(pk=receiver_account).update(balance=transferred_balance)
        except Account.DoesNotExist:
            return Response(data={"message": "Transaction failed"}, status=status.HTTP_400_BAD_REQUEST)
        Transaction.objects.create(
            account=sender_account,
            amount=amount,
            transaction_type='Transfer')
        transaction_details['receiver_account'] = receiver_account
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'Transfer'
        return Response(data=transaction_details, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return Response(data="Method not supported", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(data="Method not supported", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CheckBalance(APIView):
    def get(self,request):
        user = request.user
        account = get_object_or_404(Account, user=user.id)
        balance_details = {'account_number': account.account_number, 'balance': account.balance}
        message = f'''
        your new balance is {account.balance}
        Thank you for banking with jaguda
        '''
        send_mail(subject='JAGUDA',
                  message=message,
                  from_email='noreply@jaguda.com',
                  recipient_list=[f'{user.email}'])
        return Response(data=balance_details, status=status.HTTP_200_OK)

    @api_view()
    @login_required
    def check_balance(request):
        user = request.user
        account = get_object_or_404(Account, user=user.id)
        account_details = {'account_number': account.account_number, 'account_balance': account.account_balance}
        return Response(data=account_details, status=status.HTTP_200_OK)