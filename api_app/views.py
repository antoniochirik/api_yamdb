from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from artworks.models import Title, Review

from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        all_reviews = title.reviews.all()
        return all_reviews

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id',)
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        # review = title.reviews.get(review_id=self.kwargs.get('review_id',))
        review = get_object_or_404(
            Review,
            title=title,
            id=self.kwargs.get('review_id',)
        )
        all_comments = review.comments.all()
        return all_comments

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id',)
        )
