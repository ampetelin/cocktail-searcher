from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cocktail(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Cocktail name'))
    image_url = models.URLField(verbose_name=_('Cocktail image'))

    categories = models.ManyToManyField('Category', related_name='cocktails', verbose_name=_('Cocktail categories'))

    class Meta:
        verbose_name = _('Cocktail')
        verbose_name_plural = _('Cocktails')
        indexes = [
            GinIndex(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Category name'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Ingredient name'))

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        indexes = [
            GinIndex(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=2, verbose_name=_('Unit name'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __str__(self):
        return self.name


class Composition(models.Model):
    cocktail = models.ForeignKey(
        Cocktail, on_delete=models.CASCADE, related_name='composition', verbose_name=_('Cocktail')
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name=_('Ingredient'))
    amount = models.PositiveSmallIntegerField(verbose_name=_('Amount'))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name=_('Unit'))

    class Meta:
        verbose_name = _('Composition')
        verbose_name_plural = _('Compositions')
        constraints = [
            models.UniqueConstraint(fields=('cocktail', 'ingredient'), name='%(app_label)s_%(class)s_cpk')
        ]


class Recipe(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name='recipe', verbose_name=_('Cocktail'))
    stage = models.PositiveSmallIntegerField(verbose_name=_('Cooking stage'))
    action = models.CharField(max_length=255, verbose_name=_('Cooking action'))

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        constraints = [
            models.UniqueConstraint(fields=('cocktail', 'stage'), name='%(app_label)s_%(class)s_unique_cocktail_stage')
        ]
