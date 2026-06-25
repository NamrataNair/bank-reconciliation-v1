from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_browser, name='transactions'),
    path('manual-match/', views.manual_match, name='manual_match'),
    path('companies/', views.company_maintenance, name='company_maintenance'),
    path('bank-accounts/', views.bank_account_maintenance, name='bank_account_maintenance'),
    path('statement-upload/', views.statement_upload, name='statement_upload'),
    path('approval-queue/', views.approval_queue, name='approval_queue'),
    path('reports/', views.reports, name='reports'),
]
