from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


class IngredientInRecipeAdmin(admin.TabularInline):
    model = IngredientAmount
    fk_name = 'recipe'
    autocomplete_fields = ['ingredient']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'favorited',
                    'in_cart', 'get_tags', 'get_ingredients')
    list_display_links = list_display
    list_filter = ('author', 'name', 'tags')
    list_select_related = ('author',)

    inlines = [
        IngredientInRecipeAdmin
    ]
    autocomplete_fields = ['tags']

    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    favorited.short_description = 'Added to favorite, times'

    def in_cart(self, obj):
        return Cart.objects.filter(recipe=obj).count()
    in_cart.short_description = 'Added to cart, times'

    def get_ingredients(self, obj):
        return obj.list_ingredients()
    get_ingredients.short_description = 'Names of ingredients'

    def get_tags(self, obj):
        return obj.list_tags()
    get_tags.short_description = 'Names of tags'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(IngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
