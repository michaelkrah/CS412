# Generated by Django 5.1.3 on 2024-12-10 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anniversary', models.DateTimeField(auto_now=True)),
                ('friend1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to='music_dashboard.profile')),
                ('friend2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='music_dashboard.profile')),
            ],
        ),
    ]