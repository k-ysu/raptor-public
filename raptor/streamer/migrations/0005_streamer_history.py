# Generated by Django 2.1.7 on 2019-04-06 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0004_auto_20190406_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Streamer_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(blank=True, max_length=255, null=True)),
                ('youtube_suscribers', models.IntegerField(default=0)),
                ('youtube_total_views', models.IntegerField(default=0)),
                ('youtube_total_videos', models.IntegerField(default=0)),
                ('twitter_id', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_followers', models.IntegerField(default=0)),
                ('twitter_followings', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Game')),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Streamer')),
            ],
        ),
    ]