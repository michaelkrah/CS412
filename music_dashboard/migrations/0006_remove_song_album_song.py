# Generated by Django 5.1.3 on 2024-12-10 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_dashboard', '0005_song_spotify_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='album_song',
        ),
    ]
