from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination

from artworks.models import Title, Genre

from .serializers import ReviewSerializer, GenreSerializer
from .permissions import IsAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self, **kwargs):
        title = get_object_or_404(
            Title,
            id = self.kwargs.get('title_id',)
        )
        all_reviews = title.reviews.all()
        return all_reviews

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id',)
        )


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
