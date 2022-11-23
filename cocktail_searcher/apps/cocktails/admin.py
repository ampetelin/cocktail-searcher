from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.cocktails.models import Cocktail, Category, Ingredient, Unit, Composition, Recipe


class CompositionInline(admin.TabularInline):
    model = Composition
    verbose_name_plural = _('Cocktail composition')
    extra = 1


class RecipeInline(admin.TabularInline):
    model = Recipe
    verbose_name_plural = _('Cocktail recipe')
    extra = 1


@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin):
    inlines = (CompositionInline, RecipeInline)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    ordering = ('name',)
