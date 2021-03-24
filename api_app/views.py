
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from artworks.models import Category, Title, Genre, Review
from users.models import User
from django.core.mail import send_mail
from .tokens import account_activation_token
from .serializers import (ReviewSerializer, UserSerializer, UsernameSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer)
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


class UsersViewsSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class UsernameViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsernameSerializer


class AuthViewSet(viewsets.GenericViewSet):

    def email_confirmation(self):
        if self.request.method == 'POST':
            email = self.request.POST.get('email')
            if email is None:
                return Response("Мыло не получено")
            user = get_object_or_404(User, email=email)
            confirmation_code = account_activation_token.make_token(user)
            send_mail(
                subject='email_confirmation',
                message=confirmation_code,
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
