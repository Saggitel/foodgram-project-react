"""URL Конфигурация приложения api"""
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
