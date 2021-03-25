from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ReviewViewSet, UsersViewSet, ConfirmationCodeAPIView,
                    TitleViewSet, CategoryViewSet, GenreViewSet,
                    AuthAPIView, UserAPIView)


router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', ConfirmationCodeAPIView.as_view()),
    path('v1/auth/token/', AuthAPIView.as_view()),
    path('v1/users/', UsersViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('v1/users/<str:username>/', UsersViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('v1/users/me/', UserAPIView.as_view())
]
