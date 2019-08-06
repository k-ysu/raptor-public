from django.db import models
import pprint
from django.conf import settings

# Create your models here.
class Game(models.Model):

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

    game_name = models.CharField(max_length=100)
    game_name_jp = models.CharField(max_length=100, null=True)
    game_name_sys = models.CharField(max_length=100, null=True, db_index=True)
    game_category = models.SmallIntegerField(
        choices=GAME_CATEGORY,
        default=CATEGORY_OTHER,
    )
    game_image = models.ImageField(upload_to='streamer', null=True, blank=True)
    game_icon = models.ImageField(upload_to='streamer', null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def game_name_global(self):

        if settings.SERVER_SERVICE == 'jp':
            return self.game_name_jp
        else:
            return self.game_name

    def __str__(self):
        return self.game_name
