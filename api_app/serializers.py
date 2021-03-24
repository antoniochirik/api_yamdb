from rest_framework import serializers

from artworks.models import Comment, Review


class ReviewSerializer(serializer.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
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


class CommentSerializer(serializer.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Comment
        fields = '__all__'
