from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def transaction_browser(request):
    return render(request, 'transaction_browser.html')

def manual_match(request):
    return render(request, 'manual_match.html')
