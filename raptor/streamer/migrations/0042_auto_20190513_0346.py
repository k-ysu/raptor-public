# Generated by Django 2.1.7 on 2019-05-13 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0041_streamer_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamer_rank',
            name='streamer_thumbnail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='streamer_rank_tmp',
            name='streamer_thumbnail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
