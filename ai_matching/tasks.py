from celery import shared_task
from reconciliation.models import BankTransaction, SourceTransaction
from ai_matching.models import MatchSuggestion
from ai_matching.services import AIFactory
import datetime

@shared_task
def generate_ai_match_suggestions():
    service = AIFactory.get_service()

    # Get recent unmatched transactions
    unmatched_banks = BankTransaction.objects.filter(status='UNMATCHED')[:10]
    unmatched_sources = SourceTransaction.objects.filter(status='UNMATCHED')[:10]

    for bank_tx in unmatched_banks:
        for source_tx in unmatched_sources:
            # Skip if they obviously don't match on amount (for efficiency)
            if abs(bank_tx.amount - source_tx.amount) > 10:
                continue

            # Serialize data for the prompt
            bank_data = {
                "date": str(bank_tx.date),
                "description": bank_tx.description,
                "amount": float(bank_tx.amount),
                "type": bank_tx.type
            }
            source_data = {
                "date": str(source_tx.date),
                "description": source_tx.description,
                "amount": float(source_tx.amount),
                "type": source_tx.type
            }

            try:
                result = service.get_match_suggestion(bank_data, source_data)
                confidence = result.get('confidence_score', 0.0)

                # Only save suggestions with reasonable confidence
                if confidence > 0.5:
                    MatchSuggestion.objects.create(
                        bank_transaction=bank_tx,
                        source_transaction=source_tx,
                        confidence_score=confidence,
                        ml_model_version=result.get('model_version', 'unknown')
                    )
            except Exception as e:
                print(f"Error generating suggestion: {e}")

    return "AI matching complete"
