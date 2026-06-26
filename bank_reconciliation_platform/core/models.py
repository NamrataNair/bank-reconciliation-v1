from django.db import models

class Company(models.Model):
    company_code = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=3, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_code} - {self.company_name}"


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    branch_code = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company', 'branch_code')

    def __str__(self):
        return f"{self.branch_name} ({self.company.company_code})"


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    department_code = models.CharField(max_length=50)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company', 'department_code')

    def __str__(self):
        return f"{self.department_name} ({self.company.company_code})"


class Bank(models.Model):
    bank_code = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bank_name


class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bank_accounts')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=50, unique=True)
    account_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, default='INR')
    opening_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank.bank_name} - {self.account_number}"
