# Generated by Django 2.1.7 on 2019-04-14 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0028_auto_20190414_2135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtube_history',
            old_name='youtube_video_id',
            new_name='youtube_video',
        ),
    ]
