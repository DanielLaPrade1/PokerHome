# Generated by Django 5.0.6 on 2024-06-13 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0005_game_alter_member_ranking_club_games'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='date',
        ),
        migrations.RemoveField(
            model_name='game',
            name='elapsed_time',
        ),
    ]
