from django.test import TestCase
from decimal import Decimal
from core.models import Company, Bank, BankAccount
from .models import ImportBatch, BankTransaction, SourceTransaction, ReconciliationGroup, ReconciliationItem
from .tasks import process_import_batch, auto_match_transactions

class ReconciliationModelsTest(TestCase):
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
        self.batch = ImportBatch.objects.create(
            file_name='statement.csv',
            file_type='CSV',
            total_records=10
        )

    def test_import_batch_creation(self):
        self.assertEqual(self.batch.status, 'PENDING')
        self.assertTrue('statement.csv' in str(self.batch))

    def test_bank_transaction_creation(self):
        tx = BankTransaction.objects.create(
            batch=self.batch,
            bank_account=self.bank_account,
            date='2023-10-01',
            description='Test Deposit',
            amount=Decimal('100.50'),
            type='CR'
        )
        self.assertEqual(tx.status, 'UNMATCHED')
        self.assertEqual(tx.amount, Decimal('100.50'))

    def test_source_transaction_creation(self):
        stx = SourceTransaction.objects.create(
            company=self.company,
            source_type='UPI',
            date='2023-10-01',
            description='Test Payment',
            amount=Decimal('100.50'),
            type='CR'
        )
        self.assertEqual(stx.status, 'UNMATCHED')

    def test_reconciliation_group(self):
        group = ReconciliationGroup.objects.create(match_type='ONE_TO_ONE')
        self.assertEqual(group.status, 'DRAFT')

        tx = BankTransaction.objects.create(
            batch=self.batch,
            bank_account=self.bank_account,
            date='2023-10-01',
            description='Test',
            amount=Decimal('100'),
            type='CR'
        )
        stx = SourceTransaction.objects.create(
            company=self.company,
            source_type='UPI',
            date='2023-10-01',
            description='Test',
            amount=Decimal('100'),
            type='CR'
        )

        item = ReconciliationItem.objects.create(
            group=group,
            bank_transaction=tx,
            source_transaction=stx
        )
        self.assertEqual(item.group, group)

class ReconciliationTasksTest(TestCase):
    def test_process_import_batch_task(self):
        # Test the task stub
        result = process_import_batch(1)
        self.assertTrue(result)

    def test_auto_match_transactions_task(self):
        # Test the task stub
        result = auto_match_transactions()
        self.assertTrue(result)
