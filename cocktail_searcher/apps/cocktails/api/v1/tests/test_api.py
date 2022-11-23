from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cocktails.api.v1.serializers import RecipeSerializer
from apps.cocktails.models import Cocktail, Recipe


class RecipeTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)

    def test_get_cocktail_recipe(self):
        cocktail = baker.make(Cocktail)
        recipe = baker.make(Recipe, cocktail=cocktail, _quantity=2)
        recipe = sorted(recipe, key=lambda x: x.stage)

        url = reverse('cocktail-recipe', args=[cocktail.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.status_code)
        self.assertEqual(response.data, RecipeSerializer(recipe, many=True).data, msg=response.data)

    def test_get_cocktail_recipe_cocktail_not_found(self):
        url = reverse('cocktail-recipe', args=[1])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.status_code)
