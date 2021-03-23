from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'review',
        blank = True
    )
    score = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        autho_now_add=True
    )