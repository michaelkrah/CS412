# Generated by Django 5.1.3 on 2024-12-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_dashboard', '0006_remove_song_album_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listen',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
