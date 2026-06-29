from django.db import models
from core.models import User

class ReportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    parameters = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, PROCESSING, COMPLETED, FAILED
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.report_type} by {self.user.username} at {self.requested_at}"
