from django.db import models
from core.models import User

class ReportRequest(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=100)
    parameters = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, default='PENDING') # PENDING, PROCESSING, COMPLETED, FAILED
    file_url = models.URLField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.report_type} requested by {self.requested_by.username} at {self.requested_at}"
