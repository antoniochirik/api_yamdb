from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 1, 'user'
        MODERATOR = 2, 'moderator'
        ADMIN = 3, 'admin'
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField()
    role = models.PositiveSmallIntegerField(choices=Role.choices,
                                            default=Role.USER)
