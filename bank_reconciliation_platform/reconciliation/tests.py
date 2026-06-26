from django.test import TestCase
from django.utils import timezone
from core.models import Company, Bank, BankAccount
from .models import ImportBatch, BankTransaction, SourceTransaction

class ReconciliationModelsTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            company_code="COMP02",
            company_name="Test Company 2",
            currency="USD"
        )
        self.bank = Bank.objects.create(
            bank_code="BNK02",
            bank_name="Test Bank 2"
        )
        self.bank_account = BankAccount.objects.create(
            company=self.company,
            bank=self.bank,
            account_number="0987654321",
            account_type="CURRENT"
        )
        self.batch = ImportBatch.objects.create(
            file_name="test_file.csv",
            bank_account=self.bank_account,
            status="PENDING"
        )

    def test_import_batch_creation(self):
        self.assertEqual(self.batch.file_name, "test_file.csv")
        self.assertTrue(str(self.batch).startswith("Batch"))

    def test_bank_transaction_creation(self):
        tx = BankTransaction.objects.create(
            batch=self.batch,
            bank_account=self.bank_account,
            transaction_date=timezone.now().date(),
            description="Test Tx",
            reference_number="REF001",
            amount=100.00
        )
        self.assertEqual(tx.amount, 100.00)
        self.assertEqual(tx.status, "UNMATCHED")

    def test_source_transaction_creation(self):
        tx = SourceTransaction.objects.create(
            source_type="BANK",
            transaction_date=timezone.now().date(),
            description="Test Source Tx",
            reference_number="SRC001",
            amount=100.00
        )
        self.assertEqual(tx.amount, 100.00)
        self.assertEqual(tx.status, "UNMATCHED")

from .matching import match_one_to_one

class MatchingTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            company_code="COMP03",
            company_name="Test Company 3",
            currency="USD"
        )
        self.bank = Bank.objects.create(
            bank_code="BNK03",
            bank_name="Test Bank 3"
        )
        self.bank_account = BankAccount.objects.create(
            company=self.company,
            bank=self.bank,
            account_number="1111111111",
            account_type="CURRENT"
        )
        self.batch = ImportBatch.objects.create(
            file_name="test_file2.csv",
            bank_account=self.bank_account,
            status="COMPLETED"
        )

        # Create a bank transaction
        self.b_tx = BankTransaction.objects.create(
            batch=self.batch,
            bank_account=self.bank_account,
            transaction_date=timezone.now().date(),
            description="Matching Test TX",
            reference_number="MATCHER-001",
            amount=500.00
        )

        # Create a matching source transaction
        self.s_tx = SourceTransaction.objects.create(
            source_type="BANK",
            transaction_date=timezone.now().date(),
            description="Matching Test Source TX",
            reference_number="MATCHER-001",
            amount=500.00
        )

    def test_one_to_one_matching(self):
        # Initial state should be UNMATCHED
        self.assertEqual(self.b_tx.status, 'UNMATCHED')
        self.assertEqual(self.s_tx.status, 'UNMATCHED')

        # Run match
        matches = match_one_to_one()

        # Verify 1 match was found
        self.assertEqual(matches, 1)

        # Refresh from db
        self.b_tx.refresh_from_db()
        self.s_tx.refresh_from_db()

        # Status should be updated
        self.assertEqual(self.b_tx.status, 'MATCHED')
        self.assertEqual(self.s_tx.status, 'MATCHED')
