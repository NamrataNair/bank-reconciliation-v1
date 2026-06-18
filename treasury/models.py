from django.db import models
from core.models import Company, BankAccount

class TreasuryPosition(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateField()
    projected_balance = models.DecimalField(max_digits=15, decimal_places=2)
    actual_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    variance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} - {self.date} - {self.projected_balance}"
