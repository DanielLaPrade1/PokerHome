# Generated by Django 5.0.6 on 2024-08-12 20:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0029_alter_createduser_email_alter_createduser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createduser',
            name='phone',
            field=models.CharField(blank=True, default='No Known Number', max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid Phone Number', regex='^(\\d{10}|\\d{3}-\\d{3}-\\d{4})$')]),
        ),
    ]
