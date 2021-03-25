from rest_framework import viewsets, permissions, mixins, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from artworks.models import Category, Title, Genre
from users.models import CustomUser
from django.core.mail import send_mail
from .tokens import account_activation_token
from .serializers import (ReviewSerializer, CustomUserSerializer,
                          TitleSerializer, GenreSerializer,
                          CategorySerializer, UsernameSerializer,
                          UserAPIViewSerializer)
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


class ConfirmationCodeAPIView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        email = self.request.POST.get('email')
        if email is None:
            return Response('E-mail is None')
        user = get_object_or_404(CustomUser, email=email)
        code = account_activation_token.make_token(user)
        send_mail(
            subject='email_confirmation',
            message='Отправьте POST с e-mail и code на '
                    f'"auth/token" {code}',
            from_email='yamdb@ya.ru',
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
        permissions.IsAdminUser
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = 'username'


class UsernameViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsernameSerializer
    permissions_classes = [
        permissions.IsAdminUser
    ]
    http_method_names = ('delete', 'get', 'patch')
    lookup_field = 'username'
    pagination_class = None


class UserAPIView(APIView):
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        username = request.user.username
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserAPIViewSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        username = request.user.username
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserAPIViewSerializer(user,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
