from rest_framework import serializers

from apps.cocktails.models import Cocktail, Category, Composition, Recipe


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class CompositionSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.StringRelatedField(source='ingredient')
    unit_name = serializers.StringRelatedField(source='unit')

    class Meta:
        model = Composition
        fields = (
            'ingredient_name',
            'amount',
            'unit_name'
        )


class CocktailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    composition = CompositionSerializer(many=True, read_only=True)
    image_url = serializers.URLField()

    class Meta:
        model = Cocktail
        fields = (
            'id',
            'name',
            'image_url',
            'categories',
            'composition',
        )


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'stage',
            'action'
        )
