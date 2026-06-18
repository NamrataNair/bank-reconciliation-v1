from django.shortcuts import render
from core.models import Bank
from reconciliation.models import BankTransaction, SourceTransaction

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
