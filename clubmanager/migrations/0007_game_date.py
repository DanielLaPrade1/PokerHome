# Generated by Django 5.0.6 on 2024-06-13 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0006_remove_game_date_remove_game_elapsed_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
