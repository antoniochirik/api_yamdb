from rest_framework import serializers

from artworks.models import Review, Title, Category, Genre
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                             queryset=Category.objects.all())
    class Meta:
        fields = '__all__'
        model = Title

