from rest_framework import mixins, viewsets, filters

from artworks.models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    #pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    #lookup_field = 'slug'
