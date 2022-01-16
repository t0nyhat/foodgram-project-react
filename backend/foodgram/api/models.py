
from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Tag name')
    color = ColorField(default='#000000', verbose_name='Tag color')
    slug = AutoSlugField(unique=True, populate_from='name',
                         verbose_name='Tag slug')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ingredient name',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=200,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Tags',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientAmount',
        verbose_name='Ingredients',
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Description',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Cooking time',
        validators=[MinValueValidator(1, message='at least 1')],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name

    def list_tags(self):
        return list(self.tags.values_list('name', flat=True))

    def list_ingredients(self):
        return list(self.ingredients.values_list('name', flat=True))


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Minimum 1'),),
        verbose_name='Quantity',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ingredient quantity'
        verbose_name_plural = 'Ingredien quantity'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_receipe_ingredients')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_favoriterecipes')
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Recipe',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_user_recipes')
        ]
