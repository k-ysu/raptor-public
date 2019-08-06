# Generated by Django 2.1.7 on 2019-04-12 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0021_auto_20190412_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='streamer.Game'),
        ),
        migrations.AlterField(
            model_name='youtube_video',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='streamer.Game'),
        ),
    ]