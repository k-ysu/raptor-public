# Generated by Django 2.1.7 on 2019-04-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0022_auto_20190412_0603'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_name_jp',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
