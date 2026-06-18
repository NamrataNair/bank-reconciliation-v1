from rest_framework import serializers
from core.models import User, Company, Branch, Bank, BankAccount
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch, ReconciliationGroup

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
