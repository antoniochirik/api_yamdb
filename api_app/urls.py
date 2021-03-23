from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter


from .views import CategoryViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet)

urlpatterns = [

    path('v1/', include(router.urls)),

]