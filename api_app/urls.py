from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CommentViewSet, ReviewViewSet,
                    TitleViewSet, CategoryViewSet, GenreViewSet)

from rest_framework.authtoken import views


router = DefaultRouter()

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
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
