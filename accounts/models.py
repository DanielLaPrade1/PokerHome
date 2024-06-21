from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^(\d{10}|\d{3}-\d{3}-\d{4})$', message="Invalid Phone Number")
    phone = models.CharField(
        validators=[phone_regex], max_length=15, unique=True, blank=False, null=False, default='No Known Number')
