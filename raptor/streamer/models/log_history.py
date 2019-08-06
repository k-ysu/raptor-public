from django.db import models


# Create your models here.
class Log_History(models.Model):
    subjecdt = models.CharField(max_length=255, blank=True, null=True)
    log_history = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
