from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Company, Bank
from intercompany.models import IntercompanyTransaction
from realtime_banks.models import BankAPIConnection

class APIPhasesTest(APITestCase):
    def setUp(self):
        self.company1 = Company.objects.create(code='C1', name='Comp 1')
        self.company2 = Company.objects.create(code='C2', name='Comp 2')
        self.bank = Bank.objects.create(code='B1', name='Bank 1')

    def test_create_intercompany_transaction(self):
        url = '/api/intercompany-transactions/'
        data = {
            'from_company': self.company1.id,
            'to_company': self.company2.id,
            'amount': '1000.00',
            'date': '2023-11-01',
            'reference': 'INV-001'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IntercompanyTransaction.objects.count(), 1)

    def test_create_bank_api_connection(self):
        url = '/api/bank-api-connections/'
        data = {
            'bank': self.bank.id,
            'api_endpoint': 'https://api.bank1.com/v1',
            'client_id': 'client_123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BankAPIConnection.objects.count(), 1)
