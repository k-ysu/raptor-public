from django.db import models
import pprint
from .streamer import Streamer
from .game import Game
from .youtube_video import Youtube_Video


# Create your models here.
class Youtube_History(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE ,default=1)
    youtube_video = models.ForeignKey(Youtube_Video, on_delete=models.CASCADE ,default=1)
    viewCount = models.BigIntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    favoriteCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    youtube_created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
