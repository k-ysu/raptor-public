from django.db import models
from .streamer import Streamer
from .game import Game
from .youtube_video import Youtube_Video

# Create your models here.
class Youtube_Video_Rank_Tmp(models.Model):

    CATEGORY_PC = 1
    CATEGORY_MOBILE = 2
    CATEGORY_CONSOLE = 3
    CATEGORY_OTHER = 4

    GAME_CATEGORY = (
        (CATEGORY_PC, 'PC'),
        (CATEGORY_MOBILE, 'Mobile'),
        (CATEGORY_CONSOLE, 'Console'),
        (CATEGORY_OTHER, 'Other'),
    )


    youtube_video = models.ForeignKey(Youtube_Video, on_delete=models.CASCADE ,default=1)
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)

    game = models.ForeignKey(Game, on_delete=models.CASCADE ,default=1)

    game_category = models.SmallIntegerField(
        choices=GAME_CATEGORY,
        default=CATEGORY_OTHER,
    )
    game_name_sys = models.CharField(max_length=100, null=True)


    video_title = models.CharField(max_length=255, blank=True, null=True)
    is_video_title_present = models.BooleanField(default=False)
    video_thumbnail_medium = models.CharField(max_length=255, blank=True, null=True)
    viewCount = models.BigIntegerField(default=0)
    view_count_last48h = models.BigIntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    youtube_created_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    view_like_rate = models.DecimalField(max_digits=5,decimal_places=4,default=0.0000)
    view_like_rank = models.IntegerField(default=0)
    like_dislike_rate = models.DecimalField(max_digits=5,decimal_places=4,default=0.0000)
    like_dislike_rank = models.IntegerField(default=0)
    total_rank = models.IntegerField(default=0)
    total_rank_deviationValue = models.DecimalField(max_digits=6,decimal_places=4,default=0.0000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    streamer_thumbnail = models.CharField(max_length=255, blank=True, null=True)
    streamer_name = models.CharField(max_length=100 , blank=True, null=True)
    game_icon = models.ImageField(upload_to='streamer', null=True, blank=True)
