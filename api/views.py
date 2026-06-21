from rest_framework import viewsets
from core.models import User, Company, Branch, Bank, BankAccount, Role, AuditLog, SystemSetting
from reconciliation.models import (
    BankTransaction, SourceTransaction, ImportBatch, ReconciliationGroup,
    ReconciliationItem, ApprovalWorkflow, ApprovalAction, TDSEntry, InterestEntry
)
from analytics.models import ReportRequest
from .serializers import (
    UserSerializer, CompanySerializer, BranchSerializer, BankSerializer, BankAccountSerializer,
    ImportBatchSerializer, BankTransactionSerializer, SourceTransactionSerializer, ReconciliationGroupSerializer,
    RoleSerializer, AuditLogSerializer, SystemSettingSerializer, ReconciliationItemSerializer,
    ApprovalWorkflowSerializer, ApprovalActionSerializer, TDSEntrySerializer, InterestEntrySerializer,
    ReportRequestSerializer
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer

class ReconciliationItemViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationItem.objects.all()
    serializer_class = ReconciliationItemSerializer

class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer

class ApprovalActionViewSet(viewsets.ModelViewSet):
    queryset = ApprovalAction.objects.all()
    serializer_class = ApprovalActionSerializer

class TDSEntryViewSet(viewsets.ModelViewSet):
    queryset = TDSEntry.objects.all()
    serializer_class = TDSEntrySerializer

class InterestEntryViewSet(viewsets.ModelViewSet):
    queryset = InterestEntry.objects.all()
    serializer_class = InterestEntrySerializer

class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all()
    serializer_class = ReportRequestSerializer

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
