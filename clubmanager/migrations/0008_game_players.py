# Generated by Django 5.0.6 on 2024-06-17 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0007_game_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='clubmanager.member'),
        ),
    ]