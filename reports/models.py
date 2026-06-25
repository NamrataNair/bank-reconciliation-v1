from django.db import models
from core.models import User

class ReportRequest(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=100) # BANK_RECON_STATEMENT, INTEREST_REPORT, TDS_REPORT, CHARGES_REPORT, PENDING_RECON_REPORT
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='PENDING') # PENDING, PROCESSING, COMPLETED, FAILED
    file_path = models.CharField(max_length=255, blank=True, null=True)
    parameters = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.report_type} requested by {self.requested_by} at {self.requested_at}"
