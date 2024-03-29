# Generated by Django 2.1.7 on 2019-05-10 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0036_auto_20190510_0306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube_Video_Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(blank=True, max_length=255, null=True)),
                ('video_thumbnail_medium', models.CharField(blank=True, max_length=255, null=True)),
                ('viewCount', models.BigIntegerField(default=0)),
                ('view_count_last48h', models.BigIntegerField(default=0)),
                ('likeCount', models.IntegerField(default=0)),
                ('dislikeCount', models.IntegerField(default=0)),
                ('youtube_created_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('view_like_rate', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('view_like_rank', models.IntegerField(default=0)),
                ('like_dislike_rate', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('like_dislike_rank', models.IntegerField(default=0)),
                ('total_rank', models.IntegerField(default=0)),
                ('total_rank_deviationValue', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='streamer.Game')),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Streamer')),
                ('youtube_video', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='streamer.Youtube_Video')),
            ],
        ),
    ]
