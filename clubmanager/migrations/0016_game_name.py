# Generated by Django 5.0.6 on 2024-07-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0015_alter_game_buy_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
