# Generated by Django 5.0.6 on 2024-06-20 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0009_tournament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='num_players',
            field=models.IntegerField(default=None, null=True),
        ),
    ]