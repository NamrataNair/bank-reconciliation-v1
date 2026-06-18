from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Company, Bank, BankAccount

class APITest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(code='COMP01', name='Test Company')
        self.bank = Bank.objects.create(code='BANK01', name='Test Bank')
        self.bank_account = BankAccount.objects.create(
            bank=self.bank,
            company=self.company,
            account_number='1234567890',
            account_type='Savings',
            currency='INR'
        )

    def test_get_companies(self):
        url = '/api/companies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Company')

    def test_create_company(self):
        url = '/api/companies/'
        data = {'code': 'COMP02', 'name': 'New Company'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Company.objects.get(code='COMP02').name, 'New Company')

    def test_get_banks(self):
        url = '/api/banks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Bank')

    def test_get_bank_accounts(self):
        url = '/api/bank-accounts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['account_number'], '1234567890')
