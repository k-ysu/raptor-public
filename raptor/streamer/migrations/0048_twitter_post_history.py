# Generated by Django 2.1.7 on 2019-06-23 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0047_auto_20190611_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Twitter_Post_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_account', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
