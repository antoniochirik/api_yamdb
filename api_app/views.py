from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from artworks.models import Category, Genre, Review, Title
from users.models import CustomUser

from .filters import TitleFilter
from .permissions import IsAdmin, IsAuthorOrStaffOrReadOnly, IsStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          ConfirmationCodeSerializer)
from .tokens import account_activation_token
from django.config import settings


class ListCreateDestroyViewSet(mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly
    ]

    def get_queryset(self, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        return title.reviews.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        self.get_rating()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        update_review = self.update(request, *args, **kwargs)
        self.get_rating()
        return update_review

    def perform_create(self, serializer, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        serializer.save(
            author=self.request.user,
            title=title
        )
        self.get_rating()

    def get_rating(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        rating = self.get_queryset().aggregate(Avg('score'))
        title.rating = round(rating['score__avg'], 2)
        title.save(update_fields=['rating'])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly
    ]

    def get_queryset(self, **kwargs):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id',),
            id=self.kwargs.get('review_id',)
        )
        return review.comments.all()

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id',)
        )


class ConfirmationCodeAPIView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        email = serializer.data['email']
        user = get_object_or_404(CustomUser, email=email)
        code = account_activation_token.make_token(user)
        send_mail(
            subject='email_confirmation',
            message='Отправьте POST с e-mail и code на '
                    f'"auth/token" {code}',
            from_email=settings.EMAIL_FROM,
            recipient_list=[email]
        )
        return Response('Confirmation code was sent to your email')


class AuthAPIView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        email = self.request.POST.get('email')
        confirmed_code = self.request.POST.get('confirmed_code')
        user = get_object_or_404(CustomUser, email=email)
        code_check = account_activation_token.check_token(user, confirmed_code)
        if code_check:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response('Checking confirmed code is BAD',
                        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin
    ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def user_api_view(request):
    if request.method == 'GET':
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        user = request.user
        serializer = CustomUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
