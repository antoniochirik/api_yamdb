from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete = models.CASCADE,
        related_name = 'reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'reviews'
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



class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)



class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=200)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                               )

