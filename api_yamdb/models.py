from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                               related_name='genres')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                               related_name='categories')
