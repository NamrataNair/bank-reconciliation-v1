from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_browser, name='transactions'),
    path('manual-match/', views.manual_match, name='manual_match'),
]
