from django.db import models
from core.models import Bank

class BankAPIConnection(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    api_endpoint = models.URLField()
    client_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.bank.name} - {self.api_endpoint}"
