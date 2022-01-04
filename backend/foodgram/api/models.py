from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Unable to create a tag',
            ),
        ])

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

    def __str__(self):
        return {self.name}


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


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]
