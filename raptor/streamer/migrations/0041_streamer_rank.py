# Generated by Django 2.1.7 on 2019-05-12 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0040_streamer_rank_tmp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Streamer_Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streamer_name', models.CharField(max_length=100)),
                ('game_category', models.SmallIntegerField(choices=[(1, 'PC'), (2, 'Mobile'), (3, 'Console'), (4, 'Other')], default=4)),
                ('gender', models.SmallIntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1)),
                ('active', models.BooleanField(default=True)),
                ('youtube_channel_created', models.DateTimeField(blank=True, null=True)),
                ('youtube_suscribers', models.IntegerField(default=0)),
                ('total_view_count_last48h', models.BigIntegerField(default=0)),
                ('total_subscribe_count_last48h', models.IntegerField(default=0)),
                ('avg_deviation_score', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('rank_in_total', models.IntegerField(default=0)),
                ('rank_in_game', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='streamer.Game')),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Streamer')),
            ],
        ),
    ]
