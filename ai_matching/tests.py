from django.test import TestCase
from unittest.mock import patch, MagicMock
from decimal import Decimal
from core.models import Company, Bank, BankAccount
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch
from .models import MatchSuggestion
from .services import AIFactory, OllamaService
from .tasks import generate_ai_match_suggestions
from django.conf import settings

class AIServicesTest(TestCase):
    def test_factory_returns_correct_service(self):
        settings.AI_PROVIDER = 'ollama'
        service = AIFactory.get_service()
        self.assertIsInstance(service, OllamaService)

    @patch('ai_matching.services.requests.post')
    def test_ollama_service_returns_suggestion(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'response': '{"confidence_score": 0.85, "reasoning": "Matching amount and dates"}'
        }
        mock_post.return_value = mock_response

        service = OllamaService()
        result = service.get_match_suggestion({"amount": 100}, {"amount": 100})
        self.assertEqual(result['confidence_score'], 0.85)

class AITaskTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(code='COMP01', name='Test Company')
        self.bank = Bank.objects.create(code='BANK01', name='Test Bank')
        self.bank_account = BankAccount.objects.create(
            bank=self.bank,
            company=self.company,
            account_number='12345',
            account_type='Savings',
            currency='USD'
        )
        self.batch = ImportBatch.objects.create(file_name='test.csv', file_type='CSV')

        self.bank_tx = BankTransaction.objects.create(
            batch=self.batch,
            bank_account=self.bank_account,
            date='2023-11-01',
            description='Deposit from XYZ',
            amount=Decimal('500.00'),
            type='CR'
        )
        self.source_tx = SourceTransaction.objects.create(
            company=self.company,
            source_type='UPI',
            date='2023-11-01',
            description='Payment XYZ',
            amount=Decimal('500.00'),
            type='CR'
        )

    @patch('ai_matching.tasks.AIFactory.get_service')
    def test_generate_ai_match_suggestions_task(self, mock_factory):
        mock_service = MagicMock()
        mock_service.get_match_suggestion.return_value = {
            'confidence_score': 0.9,
            'model_version': 'test-model'
        }
        mock_factory.return_value = mock_service

        generate_ai_match_suggestions()

        self.assertEqual(MatchSuggestion.objects.count(), 1)
        suggestion = MatchSuggestion.objects.first()
        self.assertEqual(suggestion.bank_transaction, self.bank_tx)
        self.assertEqual(suggestion.source_transaction, self.source_tx)
        self.assertEqual(suggestion.confidence_score, 0.9)
