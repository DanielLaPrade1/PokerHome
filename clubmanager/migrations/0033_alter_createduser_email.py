# Generated by Django 5.0.6 on 2024-08-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0032_alter_createduser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createduser',
            name='email',
            field=models.CharField(default='No Known Email', max_length=254, verbose_name='email address'),
        ),
    ]
