from django.db import models
from core.models import User

class ReportRequest(models.Model):
    REPORT_TYPES = (
        ('BANK_RECON_STATEMENT', 'Bank Reconciliation Statement'),
        ('INTEREST_REPORT', 'Interest Report'),
        ('TDS_REPORT', 'TDS Report'),
        ('CHARGES_REPORT', 'Charges Report'),
        ('PENDING_RECON_REPORT', 'Pending Reconciliation Report'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='report_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    file_url = models.CharField(max_length=255, null=True, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.report_type} requested by {self.requested_by} at {self.requested_at}"
