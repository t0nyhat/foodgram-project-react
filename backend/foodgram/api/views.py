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
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
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

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
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

        recipes = Recipe.objects.filter(purchase__user=user).annotate(
            recipe_name=F('name'),
            recipe_text=F('text'),
            recipe_cooking_time=F('cooking_time'),
        )
        list_shop = ''
        ingredient_list = 'Ингредиенты:'
        for recipe in recipes:
            list_shop += (f'Имя рецепта: {recipe.recipe_name}\n'
                          + f'Описание: {recipe.recipe_text}\n'
                          + f'Время приготовления: {recipe.cooking_time}\n'
                          )
            ingredients = IngredientAmount.objects.filter(
                recipe_id=recipe.id)

            for item in ingredients:
                ingredient_list += (f' {item.ingredient}'
                                    + f'{item.amount}'
                                    + f'{item.ingredient.measurement_unit}'
                                    + '\n\t\t\t')
            list_shop += ingredient_list + '\n------------------------\n'
            ingredient_list = 'Ингредиенты:'

        response = HttpResponse(
            list_shop, content_type='text/plain; charset=utf-8')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)

        return response
