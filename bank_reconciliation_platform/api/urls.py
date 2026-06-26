from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, BankViewSet, BankAccountViewSet,
    ImportBatchViewSet, BankTransactionViewSet, SourceTransactionViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'banks', BankViewSet)
router.register(r'bank-accounts', BankAccountViewSet)
router.register(r'imports', ImportBatchViewSet)
router.register(r'bank-transactions', BankTransactionViewSet)
router.register(r'source-transactions', SourceTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
