# Generated by Django 5.1.3 on 2024-11-10 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='precinct_number',
            field=models.TextField(),
        ),
    ]