# Generated by Django 2.1.7 on 2019-04-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0009_auto_20190410_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube_video',
            name='youtube_tag',
            field=models.TextField(blank=True, null=True),
        ),
    ]
