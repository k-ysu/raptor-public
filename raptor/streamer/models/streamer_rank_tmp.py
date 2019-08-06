from django.db import models
from .streamer import Streamer
from .game import Game
from .youtube_video import Youtube_Video

# Create your models here.
class Streamer_Rank_Tmp(models.Model):

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


    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_OTHER = 3

    GENDER_CATEGORY = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )



    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    streamer_name = models.CharField(max_length=100)
    streamer_thumbnail = models.CharField(max_length=255, blank=True, null=True)

    game = models.ForeignKey(Game, on_delete=models.CASCADE ,default=1)
    game_category = models.SmallIntegerField(
        choices=GAME_CATEGORY,
        default=CATEGORY_OTHER,
    )
    gender = models.SmallIntegerField(
        choices=GENDER_CATEGORY,
        default=GENDER_MALE,
    )
    active = models.BooleanField(default=True)
    youtube_channel_created = models.DateTimeField(null=True, blank=True)
    youtube_suscribers = models.IntegerField(default=0)
    total_view_count_last48h = models.BigIntegerField(default=0)
    total_subscribe_count_last48h = models.IntegerField(default=0)
    avg_deviation_score = models.DecimalField(max_digits=6,decimal_places=4,default=0.0000)
    rank_in_total = models.IntegerField(default=0) # last 48h view base
    rank_in_game  = models.IntegerField(default=0) # last 48h view base
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
