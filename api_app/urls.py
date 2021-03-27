from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


from .views import (ReviewViewSet, UsersViewSet, ConfirmationCodeAPIView,
                    TitleViewSet, CategoryViewSet, GenreViewSet,
                    AuthAPIView, UserAPIView, CommentViewSet)



router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)



router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    CommentViewSet,
    basename='comment'
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
