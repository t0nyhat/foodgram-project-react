from functools import reduce

from django.db.models import F
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientNameFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag
from .paginator import Paginator
from .permissions import OwnerOrReadOnly
from .serializers import (CartSerializer, FavoriteRecipeSerializer,
                          FavoriteSerializer, IngredientSerializer,
                          ReceipeSerializer, TagSerializer)


class BaseViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientNameFilter


class ReceipeViewSet(viewsets.ModelViewSet):
    serializer_class = ReceipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = Paginator
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        data = {'user': user.id, 'recipe': recipe.id}
        serializer = FavoriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        data = {'user': user.id, 'recipe': recipe.id}
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        favorite = get_object_or_404(Cart, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        all_ingredients = IngredientAmount.objects.filter(
            recipe__purchase__user=user).annotate(
            ingredient_name=F('ingredient__name'),
            ingredient_amount=F('amount'),
            ingredient_measurement=F('ingredient__measurement_unit')
        )
        list = {}
        for ing in all_ingredients:
            key = f'{ing.ingredient_name},{ing.ingredient_measurement}'
            if key in list:
                list[key] = list[key] + ing.ingredient_amount
            else:
                list[key] = ing.ingredient_amount

        cart_txt = reduce(lambda x, key: x + key + '-'
                          + str(list[key]) + '\n', list, '')

        response = HttpResponse(
            cart_txt, content_type='text/plain; charset=utf-8')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)

        return response
