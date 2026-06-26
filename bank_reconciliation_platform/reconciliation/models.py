from django.db import models
from django.contrib.auth.models import User
from core.models import BankAccount

class ImportBatch(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    file = models.FileField(upload_to='imports/')
    file_name = models.CharField(max_length=255)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Batch {self.id} - {self.file_name}"


class BankTransaction(models.Model):
    STATUS_CHOICES = [
        ('UNMATCHED', 'Unmatched'),
        ('PARTIALLY_MATCHED', 'Partially Matched'),
        ('MATCHED', 'Matched'),
    ]
    batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE, related_name='transactions')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    value_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    reference_number = models.CharField(max_length=100, db_index=True)
    utr = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    rrn = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    balance = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNMATCHED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference_number} - {self.amount}"


class SourceTransaction(models.Model):
    SOURCE_CHOICES = [
        ('BANK', 'Bank'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('PAYROLL', 'Payroll'),
        ('AP', 'Accounts Payable'),
        ('AR', 'Accounts Receivable'),
        ('TAX', 'Tax'),
        ('GATEWAY', 'Gateway'),
    ]
    STATUS_CHOICES = [
        ('UNMATCHED', 'Unmatched'),
        ('PARTIALLY_MATCHED', 'Partially Matched'),
        ('MATCHED', 'Matched'),
    ]
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    transaction_date = models.DateField()
    description = models.TextField()
    reference_number = models.CharField(max_length=100, db_index=True)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNMATCHED')
    created_at = models.DateTimeField(auto_now_add=True)

    # UPI/Gateway specifics
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    rrn = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    settlement_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    payer_name = models.CharField(max_length=255, null=True, blank=True)
    gateway_fee = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    gst = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    net_settlement = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return f"{self.source_type} - {self.reference_number} - {self.amount}"


class ReconciliationGroup(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PREPARED', 'Prepared'),
        ('REVIEWED', 'Reviewed'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Group {self.id} - {self.status}"


class ReconciliationItem(models.Model):
    group = models.ForeignKey(ReconciliationGroup, on_delete=models.CASCADE, related_name='items')
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    source_transaction = models.ForeignKey(SourceTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    amount_matched = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return f"Item {self.id} for Group {self.group_id}"


class ApprovalWorkflow(models.Model):
    group = models.OneToOneField(ReconciliationGroup, on_delete=models.CASCADE, related_name='workflow')
    current_state = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApprovalAction(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='actions')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50) # Approve, Reject, Send Back
    comments = models.TextField(null=True, blank=True)
    action_date = models.DateTimeField(auto_now_add=True)


class TDSEntry(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE)
    tds_amount = models.DecimalField(max_digits=20, decimal_places=4)
    tds_type = models.CharField(max_length=50) # TDS on Interest, Customer TDS
    created_at = models.DateTimeField(auto_now_add=True)


class InterestEntry(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE)
    interest_amount = models.DecimalField(max_digits=20, decimal_places=4)
    interest_type = models.CharField(max_length=50) # Savings Interest, FD Interest
    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} at {self.timestamp}"
