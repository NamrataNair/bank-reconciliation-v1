from django.test import TestCase, Client
from django.urls import reverse
from .models import Company, Bank, BankAccount

class CoreModelsTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(code='COMP01', name='Test Company')
        self.bank = Bank.objects.create(code='BANK01', name='Test Bank')

    def test_company_creation(self):
        self.assertEqual(self.company.name, 'Test Company')
        self.assertEqual(str(self.company), 'COMP01 - Test Company')

    def test_bank_creation(self):
        self.assertEqual(self.bank.name, 'Test Bank')
        self.assertEqual(str(self.bank), 'Test Bank')

    def test_bank_account_creation(self):
        account = BankAccount.objects.create(
            bank=self.bank,
            company=self.company,
            account_number='1234567890',
            account_type='Savings',
            currency='INR',
            opening_balance=1000.00
        )
        self.assertEqual(account.account_number, '1234567890')
        self.assertEqual(str(account), 'Test Bank - 1234567890')

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_view(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_transactions_view(self):
        url = reverse('transactions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_browser.html')

    def test_manual_match_view(self):
        url = reverse('manual_match')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manual_match.html')
