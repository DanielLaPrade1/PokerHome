# Generated by Django 5.0.6 on 2024-08-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0016_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='ordinal_ranking',
            field=models.CharField(default='N/A', max_length=30),
        ),
    ]