from django.db import models
import pprint
from .game import Game


# Create your models here.
class Streamer(models.Model):

    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_OTHER = 3

    GENDER_CATEGORY = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )


    streamer_name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE , default=1)
    #gender = models.ForeignKey(Gender, on_delete=models.CASCADE,default=1)
    gender = models.SmallIntegerField(
        choices=GENDER_CATEGORY,
        default=GENDER_MALE,
    )
    youtube_channel_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    twitter_id = models.CharField(max_length=255, blank=True, null=True , unique=True)
    twitch_channel_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True )
    youtube_upload_list_id = models.CharField(max_length=255, blank=True, null=True)
    youtube_suscribers = models.IntegerField(default=0)
    youtube_total_views = models.BigIntegerField(default=0)
    youtube_total_videos = models.IntegerField(default=0)
    youtube_channel_created = models.DateTimeField(null=True, blank=True)
    last_youtube_uploaded = models.DateTimeField(null=True, blank=True)
    will_update_popular_video = models.BooleanField(default=True)
    twitter_followers = models.IntegerField(default=0)
    twitter_followings = models.IntegerField(default=0)
    streamer_thumbnail = models.CharField(max_length=255, blank=True, null=True)
    streamer_banner = models.CharField(max_length=255, blank=True, null=True)
    streamer_description = models.TextField(blank=True, null=True)
    is_ready = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} : {}'.format(self.id, self.streamer_name)
