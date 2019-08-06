from django.db import models


# Create your models here.
class Twitter_Post_History(models.Model):
    twitter_account = models.CharField(max_length=255)
    url = models.CharField(max_length=255, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
