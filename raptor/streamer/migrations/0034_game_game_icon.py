# Generated by Django 2.1.7 on 2019-05-06 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0033_game_game_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_icon',
            field=models.ImageField(blank=True, null=True, upload_to='streamer'),
        ),
    ]