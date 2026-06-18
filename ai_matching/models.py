from django.db import models
from reconciliation.models import BankTransaction, SourceTransaction

class MatchSuggestion(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE)
    source_transaction = models.ForeignKey(SourceTransaction, on_delete=models.CASCADE)
    confidence_score = models.FloatField()
    suggested_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    ml_model_version = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Suggestion {self.bank_transaction.id} <-> {self.source_transaction.id} ({self.confidence_score})"
