from rest_framework import serializers
from core.models import User, Company, Branch, Bank, BankAccount, Role, SystemSetting, AuditLog, ReportRequest
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch, ReconciliationGroup, ReconciliationItem, ApprovalWorkflow, ApprovalAction, TDSEntry, InterestEntry

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class ReportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRequest
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class ImportBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportBatch
        fields = '__all__'

class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = '__all__'

class SourceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceTransaction
        fields = '__all__'

class ReconciliationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationGroup
        fields = '__all__'

class ReconciliationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationItem
        fields = '__all__'

class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'

class ApprovalActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalAction
        fields = '__all__'

class TDSEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TDSEntry
        fields = '__all__'

class InterestEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestEntry
        fields = '__all__'
