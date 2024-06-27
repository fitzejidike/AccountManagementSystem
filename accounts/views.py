from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, Transaction
from .serializers import AccountSerializer, AccountCreateSerializer


class ListAccount(ListCreateAPIView):
    def get_queryset(self):
        return Account.objects.all()

    def get_serializer_class(self):
        return AccountCreateSerializer

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetails(APIView):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        if request.method == 'GET':
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = AccountCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#
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
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def deposit(request):
    accounts_number = request.data['account_number']
    amount = request.data['amount']
    account = get_object_or_404(Account, pk=accounts_number)
    account.balance += Decimal(amount)
    account.save()
    Transaction.objects.create(account=account,
                               amount=amount)
    return Response(data={"message": "Transaction success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def withdraw(request):
    accounts_number = request.data['account_number']
    amount = request.data.get['amount', "amount cannot be null"]
    pin = request.data['pin']
    account = get_object_or_404(Account, pk=accounts_number)
    if account.pin == pin:
        if account.balance > amount:
            account.balance -= Decimal(amount)
            account.save()
        else:
            return Response(data={"message": "Invalid:Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    else:

        return Response(data={"message": "Invalid: Invalid Transaction"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={"message": "Transaction success"}, status=status.HTTP_200_OK)
