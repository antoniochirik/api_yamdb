# from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver

User = get_user_model()

# class Profile(models.Model):

#     class Role(models.TextChoices):
#         USER = 1, 'user'
#         MODERATOR = 2, 'moderator'
#         ADMIN = 3, 'admin'

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     email = models.EmailField()
#     role = models.PositiveSmallIntegerField(choices=Role.choices,
#                                             default=Role.USER)


# @receiver(post_save, sender=User)
# def create_custom_user(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_custom_user(sender, instance, **kwargs):
#     instance.profile.save()
