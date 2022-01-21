import django_filters as filters
from django.contrib.auth import get_user_model

from .models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    IN = 1
    OUT = 0
    CHOICES = (
        (IN, 1),
        (OUT, 0),
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug')

    is_favorited = filters.ChoiceFilter(
        method='get_is_favorited',
        choices=CHOICES
    )
    filters.ChoiceFilter
    is_in_shopping_cart = filters.ChoiceFilter(
        method='get_is_in_shopping_cart',
        choices=CHOICES
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        print(value)

        if value:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(purchase__user=user)
        return queryset
