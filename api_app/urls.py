from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet


from .views import CommentViewSet, ReviewViewSet


router = DefaultRouter()

router.register('titles', TitleViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    CommentViewSet,
    basename='comment'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
