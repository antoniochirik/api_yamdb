from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from .views import TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet


router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles',
    TitleViewSet,
    basename='title'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]