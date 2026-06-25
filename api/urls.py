from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_phases import (
    ExceptionCaseViewSet, MatchSuggestionViewSet, JournalEntryViewSet,
    IntercompanyTransactionViewSet, TreasuryPositionViewSet, BankAPIConnectionViewSet
)

from .views import (
    UserViewSet, CompanyViewSet, BranchViewSet, BankViewSet, BankAccountViewSet,
    ImportBatchViewSet, BankTransactionViewSet, SourceTransactionViewSet, ReconciliationGroupViewSet,
    RoleViewSet, SystemSettingViewSet, AuditLogViewSet, ReportRequestViewSet,
    ReconciliationItemViewSet, ApprovalWorkflowViewSet, ApprovalActionViewSet, TDSEntryViewSet, InterestEntryViewSet
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'system-settings', SystemSettingViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'report-requests', ReportRequestViewSet)
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'banks', BankViewSet)
router.register(r'bank-accounts', BankAccountViewSet)
router.register(r'import-batches', ImportBatchViewSet)
router.register(r'bank-transactions', BankTransactionViewSet)
router.register(r'source-transactions', SourceTransactionViewSet)
router.register(r'reconciliation-groups', ReconciliationGroupViewSet)
router.register(r'reconciliation-items', ReconciliationItemViewSet)
router.register(r'approval-workflows', ApprovalWorkflowViewSet)
router.register(r'approval-actions', ApprovalActionViewSet)
router.register(r'tds-entries', TDSEntryViewSet)
router.register(r'interest-entries', InterestEntryViewSet)


router.register(r'exceptions', ExceptionCaseViewSet)
router.register(r'match-suggestions', MatchSuggestionViewSet)
router.register(r'journal-entries', JournalEntryViewSet)
router.register(r'intercompany-transactions', IntercompanyTransactionViewSet)
router.register(r'treasury-positions', TreasuryPositionViewSet)
router.register(r'bank-api-connections', BankAPIConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
