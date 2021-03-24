from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Title(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Напишите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        blank=True, 
        help_text='Укажите год создания'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True, null=True,
        help_text='Добавьте сюда описание произведения'
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True
    )
