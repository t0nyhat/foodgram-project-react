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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    filterset_class = IngredientNameFilter


class ReceipeViewSet(viewsets.ModelViewSet):
    serializer_class = ReceipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = Paginator
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
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
        favorite = get_object_or_404(
            Favorite, user=user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
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
        favorite = get_object_or_404(
            Cart, user=user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(cart__user=user)
        queryset = IngredientAmount.objects.filter(recipe_id__in=recipes)
        shopping_list = {}
        list_shop = ''
        for recipe in recipes.values('id', 'name', 'text', 'cooking_time'):

            list_shop += '\t'.join([f'{key}:{value}' for key,
                                   value in recipe.items() if key != 'id'])
            ingredients = IngredientAmount.objects.filter(
                recipe_id=recipe['id'])
            print(ingredients.values())

        print(list_shop)

        for ingredient in queryset:
            name = ingredient.ingredient.name
            amount = ingredient.amount
            if name in shopping_list:
                shopping_list[name] = shopping_list[name] + amount
            else:
                shopping_list[name] = amount
        plain_list = ''
        for item in shopping_list.keys():
            plain_list += f'{item}: {shopping_list[item]}\n'
        response = HttpResponse(plain_list,
                                content_type='text/plain; charset=utf-8')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = ('attachment; filename={0}'.
                                           format(filename))
        return HttpResponse(response)
