from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from artworks.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'slug'
        exclude = ['id']
        model = Category



class CategoryField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategorySerializer(value).data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'slug'
        exclude = ['id']
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenreSerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()


    def get_rating(self, obj):
        avg_dict = obj.reviews.aggregate(Avg('score'))
        return avg_dict['score__avg']


    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        author = self.context.get('request').user
        title = get_object_or_404(
            Title,
            id=self.context.get('view').kwargs.get('title_id')
        )
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(title=title,
                                      author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'You have already left review about this title'})
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)

    def validate(self, data):
        get_object_or_404(
            Review,
            title_id=self.context.get('view').kwargs.get('title_id'),
            id=self.context.get('view').kwargs.get('review_id')
        )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )

    def validate(self, data):
        email = self.request.POST.get('email')
        if email is None:
            raise(serializers.ValidationError('E-mail is None'))
        return data
