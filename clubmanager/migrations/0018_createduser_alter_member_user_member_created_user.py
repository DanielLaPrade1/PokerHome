# Generated by Django 5.0.6 on 2024-08-12 18:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubmanager', '0017_member_ordinal_ranking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, verbose_name='email address')),
                ('phone', models.CharField(blank=True, default='No Known Number', max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Phone Number', regex='^(\\d{10}|\\d{3}-\\d{3}-\\d{4})$')])),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='member',
            name='created_user',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='clubmanager.createduser'),
        ),
    ]
