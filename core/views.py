from django.shortcuts import render
from core.models import Bank, Company, BankAccount
from reconciliation.models import BankTransaction, SourceTransaction, ImportBatch, ApprovalWorkflow

def dashboard(request):
    total_tx = BankTransaction.objects.count() + SourceTransaction.objects.count()
    matched_tx = BankTransaction.objects.filter(status='MATCHED').count() + SourceTransaction.objects.filter(status='MATCHED').count()
    pending_tx = BankTransaction.objects.filter(status='UNMATCHED').count() + SourceTransaction.objects.filter(status='UNMATCHED').count()

    match_percentage = 0
    if total_tx > 0:
        match_percentage = int((matched_tx / total_tx) * 100)

    context = {
        'total_tx': total_tx,
        'matched_tx': matched_tx,
        'pending_tx': pending_tx,
        'match_percentage': match_percentage
    }
    return render(request, 'dashboard.html', context)

def transaction_browser(request):
    # HTMX request handling
    if request.htmx:
        bank_id = request.GET.get('bank')
        status = request.GET.get('status')
        date = request.GET.get('date')

        transactions = BankTransaction.objects.all()
        if bank_id:
            transactions = transactions.filter(bank_account__bank_id=bank_id)
        if status:
            transactions = transactions.filter(status=status)
        if date:
            transactions = transactions.filter(date=date)

        return render(request, 'partials/transaction_list.html', {'transactions': transactions})

    banks = Bank.objects.all()
    transactions = BankTransaction.objects.all()
    return render(request, 'transaction_browser.html', {'banks': banks, 'transactions': transactions})

def manual_match(request):
    bank_tx = BankTransaction.objects.filter(status='UNMATCHED')
    source_tx = SourceTransaction.objects.filter(status='UNMATCHED')
    return render(request, 'manual_match.html', {'bank_tx': bank_tx, 'source_tx': source_tx})

def company_maintenance(request):
    companies = Company.objects.all()
    return render(request, 'company_maintenance.html', {'companies': companies})

def bank_account_maintenance(request):
    bank_accounts = BankAccount.objects.all()
    return render(request, 'bank_account_maintenance.html', {'bank_accounts': bank_accounts})

def statement_upload(request):
    if request.method == 'POST':
        # Handle file upload logic here
        pass
    import_batches = ImportBatch.objects.all()
    return render(request, 'statement_upload.html', {'import_batches': import_batches})

def approval_queue(request):
    if request.method == 'POST':
        # Handle approval/rejection logic here
        pass
    workflows = ApprovalWorkflow.objects.all()
    return render(request, 'approval_queue.html', {'workflows': workflows})

def reports(request):
    if request.method == 'POST':
        # Handle report generation logic here
        pass
    return render(request, 'reports.html')
