from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


class IngredientInRecipeAdmin(admin.TabularInline):
    """Класс для отображения таблицы c ингредиентами в админке рецепта."""

    model = IngredientAmount
    fk_name = "recipe"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "favorited")
    list_filter = ("author", "name", "tags")
    exclude = ("ingredients",)

    inlines = [
        IngredientInRecipeAdmin,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = "В избранном"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("^name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(IngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")
