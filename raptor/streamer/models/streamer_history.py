from django.db import models
import pprint
from .streamer import Streamer
from .game import Game

# Create your models here.
class Streamer_History(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    youtube_channel_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    youtube_suscribers = models.IntegerField(default=0)
    youtube_total_views = models.BigIntegerField(default=0)
    youtube_total_videos = models.IntegerField(default=0)
    twitter_id = models.CharField(max_length=255, blank=True, null=True)
    twitter_followers = models.IntegerField(default=0)
    twitter_followings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
