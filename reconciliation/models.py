from django.db import models
from core.models import User, BankAccount, Company

class ImportBatch(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10) # CSV, XLSX, MT940
    status = models.CharField(max_length=50, default='PENDING') # PENDING, PROCESSING, COMPLETED, FAILED
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.file_name} - {self.uploaded_at}"

class BankTransaction(models.Model):
    batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE, related_name='bank_transactions')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    utr = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=10) # DR or CR
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='UNMATCHED') # UNMATCHED, MATCHED, RECONCILED

    def __str__(self):
        return f"{self.bank_account} - {self.date} - {self.amount}"

class SourceTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=50) # UPI, CARD, PAYROLL, AP, AR, TAX, GATEWAY
    date = models.DateField()
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    rrn = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=10) # DR or CR
    status = models.CharField(max_length=20, default='UNMATCHED') # UNMATCHED, MATCHED, RECONCILED

    def __str__(self):
        return f"{self.source_type} - {self.date} - {self.amount}"

class ReconciliationGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    match_type = models.CharField(max_length=50) # ONE_TO_ONE, ONE_TO_MANY, MANY_TO_ONE, MANY_TO_MANY
    status = models.CharField(max_length=20, default='DRAFT') # DRAFT, PENDING_APPROVAL, APPROVED, REJECTED

    def __str__(self):
        return f"Group {self.id} - {self.match_type}"

class ReconciliationItem(models.Model):
    group = models.ForeignKey(ReconciliationGroup, on_delete=models.CASCADE, related_name='items')
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE, null=True, blank=True)
    source_transaction = models.ForeignKey(SourceTransaction, on_delete=models.CASCADE, null=True, blank=True)

class ApprovalWorkflow(models.Model):
    group = models.ForeignKey(ReconciliationGroup, on_delete=models.CASCADE, related_name='workflows')
    state = models.CharField(max_length=50, default='DRAFT') # DRAFT, PREPARED, REVIEWED, APPROVED
    updated_at = models.DateTimeField(auto_now=True)

class ApprovalAction(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='actions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50) # APPROVE, REJECT, SEND_BACK
    comments = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class TDSEntry(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tds_type = models.CharField(max_length=50) # TDS_ON_INTEREST, CUSTOMER_TDS
    date = models.DateField()

class InterestEntry(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_type = models.CharField(max_length=50) # SAVINGS, FD
    date = models.DateField()
