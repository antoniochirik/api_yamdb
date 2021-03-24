from rest_framework import serializers

from posts.models import Review, Title, Category, Genre



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



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Genre

        
class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                             queryset=Category.objects.all())
    class Meta:
        fields = '__all__'
        model = Title

