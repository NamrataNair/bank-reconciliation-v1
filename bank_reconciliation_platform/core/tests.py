from django.test import TestCase
from .models import Company, Bank, BankAccount

class CoreModelsTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            company_code="COMP01",
            company_name="Test Company",
            currency="USD"
        )
        self.bank = Bank.objects.create(
            bank_code="BNK01",
            bank_name="Test Bank"
        )
        self.bank_account = BankAccount.objects.create(
            company=self.company,
            bank=self.bank,
            account_number="1234567890",
            account_type="SAVINGS"
        )

    def test_company_creation(self):
        self.assertEqual(self.company.company_name, "Test Company")
        self.assertEqual(str(self.company), "COMP01 - Test Company")

    def test_bank_creation(self):
        self.assertEqual(self.bank.bank_name, "Test Bank")
        self.assertEqual(str(self.bank), "Test Bank")

    def test_bank_account_creation(self):
        self.assertEqual(self.bank_account.account_number, "1234567890")
        self.assertEqual(str(self.bank_account), "Test Bank - 1234567890")
