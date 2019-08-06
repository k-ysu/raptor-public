from django.db import models
import pprint
from .game import Game


# Create your models here.


class Game_Tag(models.Model):

    PRIORITY_HIGH = 3
    PRIORITY_MIDDLE = 5
    PRIORITY_LOW = 7
    PRIORITY_CATEGORY = (
        (PRIORITY_HIGH, '3 : High'),
        (PRIORITY_MIDDLE, '5 : Middle'),
        (PRIORITY_LOW, '7 : Low'),

    )


    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=1)
    game_tag = models.CharField(max_length=100)
    priority = models.SmallIntegerField(
        choices=PRIORITY_CATEGORY,
        default=PRIORITY_MIDDLE,
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game_tag
