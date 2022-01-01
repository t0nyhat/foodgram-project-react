from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    color = ColorField(unique=True, default='#FF0000')
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
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=200,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return {self.name}
