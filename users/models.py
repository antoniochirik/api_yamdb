from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        USER = 'USR', 'user'
        MODERATOR = 'MDR', 'moderator'
        ADMIN = 'ADM', 'admin'

    email = models.EmailField('e-mail', unique=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=3, choices=Role.choices,
                            default=Role.USER)
    confirmed_code = models.CharField(max_length=24, blank=True)
