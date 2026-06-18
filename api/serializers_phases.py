from rest_framework import serializers
from exception_management.models import ExceptionCase
from ai_matching.models import MatchSuggestion
from journal_entries.models import JournalEntry, JournalEntryLine
from intercompany.models import IntercompanyTransaction
from treasury.models import TreasuryPosition
from realtime_banks.models import BankAPIConnection

class ExceptionCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionCase
        fields = '__all__'

class MatchSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchSuggestion
        fields = '__all__'

class JournalEntryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryLine
        fields = '__all__'

class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True, read_only=True)
    class Meta:
        model = JournalEntry
        fields = '__all__'

class IntercompanyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntercompanyTransaction
        fields = '__all__'

class TreasuryPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasuryPosition
        fields = '__all__'

class BankAPIConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAPIConnection
        fields = '__all__'
