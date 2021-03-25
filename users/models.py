from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Profile(models.Model):

    class Role(models.TextChoices):
        USER = 1, 'user'
        MODERATOR = 2, 'moderator'
        ADMIN = 3, 'admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField()
    role = models.PositiveSmallIntegerField(choices=Role.choices,
                                            default=Role.USER)


@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_custom_user(sender, instance, **kwargs):
    instance.profile.save()


# from django.core.validators import RegexValidator
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext_lazy as _


# class User(AbstractUser):
#     class Roles(models.TextChoices):
#         USER = 'user', _('user')
#         MODERATOR = 'moderator', _('moderator')
#         ADMIN = 'admin', _('admin')

#     """ 
#     Валидатор нужен чтобы в username не было символов вроде '@'
#     которые не обработаются в /users/{username}/
#     """
#     alphanumeric = RegexValidator(
#         r'^[0-9a-zA-Z_]*$',
#         'Разрешены символы алфавита, цифры и нижние подчеркивания.'
#     )

#     username = models.CharField(max_length=50, unique=True,
#                                 blank=False, null=False,
#                                 validators=[alphanumeric])
#     email = models.EmailField(unique=True, blank=False, null=False)
#     role = models.CharField(max_length=100, choices=Roles.choices, default=Roles.USER)
#     bio = models.TextField(max_length=3000, blank=True, null=True)


# class UserConfirmation(models.Model):
#     email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
#     confirmation_code = models.CharField(max_length=1000, blank=True, null=True)
