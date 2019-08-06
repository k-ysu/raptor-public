from django.db import models
import pprint
from .streamer import Streamer
from .game import Game

# Create your models here.
class Youtube_Video(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE ,default=1)
    youtube_channel_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    youtube_video_org_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, unique=True)
    youtube_tag = models.TextField(blank=True, null=True)
    video_title = models.CharField(max_length=255, blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    video_thumbnail_medium = models.CharField(max_length=255, blank=True, null=True)
    video_thumbnail_default = models.CharField(max_length=255, blank=True, null=True)
    viewCount = models.BigIntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    favoriteCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    uploadStatus = models.CharField(max_length=255, blank=True, null=True)
    privacyStatus = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    embeddable = models.BooleanField(default=True)
    publicStatsViewable = models.BooleanField(default=False)
    will_info_update = models.BooleanField(default=False)
    youtube_created_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    is_ready = models.BooleanField(default=False)
    is_low_views = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "ID :{} => {},  Title : {}".format(self.id,self.streamer.streamer_name,self.video_title)
