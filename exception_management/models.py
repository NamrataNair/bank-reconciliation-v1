from django.db import models
from core.models import User
from reconciliation.models import BankTransaction, SourceTransaction

class ExceptionCase(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE, null=True, blank=True)
    source_transaction = models.ForeignKey(SourceTransaction, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=50, default='OPEN') # OPEN, IN_PROGRESS, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Exception {self.id} - {self.status}"
