from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Administrator'

    email = models.EmailField(
        'e-mail',
        unique=True
    )
    bio = models.TextField(
        max_length=500,
        blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
