# Generated by Django 2.1.7 on 2019-06-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0044_auto_20190603_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube_video_rank',
            name='game_icon',
            field=models.ImageField(blank=True, null=True, upload_to='streamer'),
        ),
        migrations.AddField(
            model_name='youtube_video_rank_tmp',
            name='game_icon',
            field=models.ImageField(blank=True, null=True, upload_to='streamer'),
        ),
    ]