from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ReviewViewSet, UsersViewSet, ConfirmationCode,
                    TitleViewSet, CategoryViewSet, GenreViewSet,
                    Auth)


router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)


# router.register(
#     r'^titles',
#     TitleViewSet,
#     basename='title'
# )

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', ConfirmationCode.as_view(),
         name='confirmed_code'),
    path('v1/auth/token/', Auth.as_view(),
         name='token'),
    path('v1/users/', UsersViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('v1/users/<str:username>/', UsersViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }))
]
