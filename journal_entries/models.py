from django.db import models
from core.models import Company
from reconciliation.models import ReconciliationGroup

class JournalEntry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reconciliation_group = models.ForeignKey(ReconciliationGroup, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='DRAFT') # DRAFT, POSTED
    created_at = models.DateTimeField(auto_now_add=True)

class JournalEntryLine(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account_code = models.CharField(max_length=50)
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
