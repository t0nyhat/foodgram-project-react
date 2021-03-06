from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, ReceipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', ReceipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
urlpatterns = [
    path('', include(router.urls)),
]
