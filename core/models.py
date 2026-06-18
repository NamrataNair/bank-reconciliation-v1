from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users', blank=True)

class Company(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=3, default='INR')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class Bank(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='accounts')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=50, unique=True)
    account_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, default='INR')
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.bank.name} - {self.account_number}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key
