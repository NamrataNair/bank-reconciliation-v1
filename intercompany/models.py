from django.db import models
from core.models import Company

class IntercompanyTransaction(models.Model):
    from_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ic_from_transactions')
    to_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ic_to_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    date = models.DateField()
    status = models.CharField(max_length=50, default='PENDING') # PENDING, RECONCILED
    reference = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.from_company.code} -> {self.to_company.code}: {self.amount}"
