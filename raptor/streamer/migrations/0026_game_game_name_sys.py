# Generated by Django 2.1.7 on 2019-04-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0025_game_tag_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_name_sys',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
