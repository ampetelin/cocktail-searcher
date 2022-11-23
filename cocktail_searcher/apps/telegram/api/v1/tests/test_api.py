from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from apps.telegram.api.v1.serializers import TelegramUserFavoriteSerializer
from apps.telegram.models import TelegramUser, FavoriteCocktail


class TelegramUserFavoritesTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)

    def test_get_telegram_user_favorites(self):
        telegram_user = baker.make(TelegramUser)
        favorites = baker.make(FavoriteCocktail, telegram_user=telegram_user, _quantity=2)
        favorites = sorted(favorites, key=lambda x: x.created_at, reverse=True)

        url = reverse('telegramuser-favorites', args=[telegram_user.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data['results'] if api_settings.DEFAULT_PAGINATION_CLASS else response.data
        self.assertEqual(
            first=response_data,
            second=TelegramUserFavoriteSerializer(favorites, many=True).data,
            msg=response.data
        )

    def test_get_telegram_user_favorites_telegram_user_not_found(self):
        url = reverse('telegramuser-favorites', args=[1])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.status_code)
