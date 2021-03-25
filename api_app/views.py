from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from artworks.models import Category, Title, Genre
from users.models import CustomUser
from django.core.mail import send_mail
from .tokens import account_activation_token
from .serializers import (ReviewSerializer, CustomUserSerializer,
                          TitleSerializer, GenreSerializer,
                          CategorySerializer)
from .permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request):
        email = self.request.POST.get('email')
        if email is None:
            return Response('E-mail is None')
        user = get_object_or_404(CustomUser, email=email)
        confirmation_code = account_activation_token.make_token(user)
        send_mail(
            subject='email_confirmation',
            message='Отправьте POST с e-mail и code на '
                    f'"auth/token" {confirmation_code}',
            from_email='yamdb@ya.ru',
            recipient_list=[email]
        )
        return Response('Confirmation code was sent to your email')


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
