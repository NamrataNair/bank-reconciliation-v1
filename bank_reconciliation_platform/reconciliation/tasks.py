from celery import shared_task
import time
import pandas as pd
from django.utils import timezone
from .models import ImportBatch, BankTransaction
from .matching import run_auto_matching

@shared_task
def import_job(batch_id):
    print(f"Starting import job for batch: {batch_id}")
    try:
        batch = ImportBatch.objects.get(id=batch_id)
        batch.status = 'PROCESSING'
        batch.save()

        # Read the file
        if batch.file.name.endswith('.csv'):
            df = pd.read_csv(batch.file.path)
        elif batch.file.name.endswith('.xlsx') or batch.file.name.endswith('.xls'):
            df = pd.read_excel(batch.file.path)
        else:
            raise ValueError("Unsupported file format")

        transactions_to_create = []
        for index, row in df.iterrows():
            # In a real app, field mapping would be dynamic.
            # Assuming standard columns for this basic implementation:
            # Date, Description, Reference, Amount
            date_val = pd.to_datetime(row.get('Date', timezone.now())).date()
            amount_val = row.get('Amount', 0.0)
            if pd.isna(amount_val): amount_val = 0.0

            transactions_to_create.append(
                BankTransaction(
                    batch=batch,
                    bank_account=batch.bank_account,
                    transaction_date=date_val,
                    description=str(row.get('Description', '')),
                    reference_number=str(row.get('Reference', '')),
                    amount=amount_val,
                    status='UNMATCHED'
                )
            )

        BankTransaction.objects.bulk_create(transactions_to_create)

        batch.status = 'COMPLETED'
        batch.processed_at = timezone.now()
        batch.save()

        # Optionally trigger matching after import
        # auto_matching_job.delay()

    except Exception as e:
        if 'batch' in locals():
            batch.status = 'FAILED'
            batch.error_message = str(e)
            batch.save()
        print(f"Failed import job: {str(e)}")
        return False

    print(f"Completed import job for batch: {batch_id}")
    return True


@shared_task
def auto_matching_job():
    print("Starting auto matching job...")
    results = run_auto_matching()
    print(f"Completed auto matching job. Results: {results}")
    return True

@shared_task
def report_generation_job(report_type):
    print(f"Generating report: {report_type}")
    time.sleep(2)
    print("Report generation complete.")
    return True

@shared_task
def cleanup_job():
    print("Starting cleanup job...")
    time.sleep(2)
    print("Completed cleanup job.")
    return True
