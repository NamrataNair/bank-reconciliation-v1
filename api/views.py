from rest_framework import viewsets
from core.models import User, Company, Branch, Bank, BankAccount
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch, ReconciliationGroup
from .serializers import (
    UserSerializer, CompanySerializer, BranchSerializer, BankSerializer, BankAccountSerializer,
    ImportBatchSerializer, BankTransactionSerializer, SourceTransactionSerializer, ReconciliationGroupSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

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

class ReconciliationGroupViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationGroup.objects.all()
    serializer_class = ReconciliationGroupSerializer
