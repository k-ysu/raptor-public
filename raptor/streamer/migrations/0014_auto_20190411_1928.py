# Generated by Django 2.1.7 on 2019-04-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0013_youtube_video_is_category_set'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamer',
            name='active',
        ),
        migrations.AddField(
            model_name='streamer',
            name='is_information_update',
            field=models.BooleanField(default=False),
        ),
    ]
