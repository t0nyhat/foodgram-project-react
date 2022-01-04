from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .filters import IngredientNameFilter
from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, ReceipeSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    filterset_class = IngredientNameFilter


class ReceipeViewSet(viewsets.ModelViewSet):
    serializer_class = ReceipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
