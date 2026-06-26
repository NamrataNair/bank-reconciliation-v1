from django.db import transaction
from decimal import Decimal
from .models import BankTransaction, SourceTransaction, ReconciliationGroup, ReconciliationItem

def match_one_to_one():
    """
    Attempts to exact match BankTransactions and SourceTransactions based on reference_number, date and amount.
    """
    bank_txs = BankTransaction.objects.filter(status='UNMATCHED')

    matches = 0
    for b_tx in bank_txs:
        # Simple exact match logic: Amount matches, and either reference or date matches.
        # In a real system, criteria would be configurable.
        s_tx = SourceTransaction.objects.filter(
            status='UNMATCHED',
            amount=b_tx.amount,
            reference_number=b_tx.reference_number,
            transaction_date=b_tx.transaction_date
        ).first()

        if s_tx:
            with transaction.atomic():
                group = ReconciliationGroup.objects.create(status='PREPARED')

                ReconciliationItem.objects.create(
                    group=group,
                    bank_transaction=b_tx,
                    source_transaction=s_tx,
                    amount_matched=b_tx.amount
                )

                b_tx.status = 'MATCHED'
                b_tx.save()

                s_tx.status = 'MATCHED'
                s_tx.save()

                matches += 1

    return matches

def run_auto_matching():
    """
    Executes various matching algorithms in sequence.
    """
    matches_1_to_1 = match_one_to_one()
    # Placeholder for One-to-Many, Many-to-One, etc.
    return {
        "one_to_one_matches": matches_1_to_1
    }
