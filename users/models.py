from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    class Role(models.IntegerChoices):
        USER = 1, 'user'
        MODERATOR = 2, 'moderator'
        ADMIN = 3, 'admin'

    email = models.EmailField('e-mail', unique=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=9, choices=Role.choices,
                            default=Role.USER.label)

    objects = CustomUserManager()
