from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Company, Bank, BankAccount
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch
from .serializers import (
    CompanySerializer, BankSerializer, BankAccountSerializer,
    ImportBatchSerializer, BankTransactionSerializer, SourceTransactionSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

class ImportBatchViewSet(viewsets.ModelViewSet):
    queryset = ImportBatch.objects.all()
    serializer_class = ImportBatchSerializer

class BankTransactionViewSet(viewsets.ModelViewSet):
    queryset = BankTransaction.objects.all()
    serializer_class = BankTransactionSerializer

class SourceTransactionViewSet(viewsets.ModelViewSet):
    queryset = SourceTransaction.objects.all()
    serializer_class = SourceTransactionSerializer
