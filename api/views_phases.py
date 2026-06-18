from rest_framework import viewsets
from exception_management.models import ExceptionCase
from ai_matching.models import MatchSuggestion
from journal_entries.models import JournalEntry
from intercompany.models import IntercompanyTransaction
from treasury.models import TreasuryPosition
from realtime_banks.models import BankAPIConnection

from .serializers_phases import (
    ExceptionCaseSerializer, MatchSuggestionSerializer, JournalEntrySerializer,
    IntercompanyTransactionSerializer, TreasuryPositionSerializer, BankAPIConnectionSerializer
)

class ExceptionCaseViewSet(viewsets.ModelViewSet):
    queryset = ExceptionCase.objects.all()
    serializer_class = ExceptionCaseSerializer

class MatchSuggestionViewSet(viewsets.ModelViewSet):
    queryset = MatchSuggestion.objects.all()
    serializer_class = MatchSuggestionSerializer

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

class IntercompanyTransactionViewSet(viewsets.ModelViewSet):
    queryset = IntercompanyTransaction.objects.all()
    serializer_class = IntercompanyTransactionSerializer

class TreasuryPositionViewSet(viewsets.ModelViewSet):
    queryset = TreasuryPosition.objects.all()
    serializer_class = TreasuryPositionSerializer

class BankAPIConnectionViewSet(viewsets.ModelViewSet):
    queryset = BankAPIConnection.objects.all()
    serializer_class = BankAPIConnectionSerializer
