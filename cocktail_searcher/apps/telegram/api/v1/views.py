from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.telegram.api.v1.filtersets import TelegramUserFilterSet
from apps.telegram.api.v1.serializers import (
    TelegramUserSerializer,
    FavoriteCocktailSerializer,
    TelegramUserFavoriteSerializer,
)
from apps.telegram.models import TelegramUser, FavoriteCocktail


@extend_schema(tags=['Telegram Users'])
class TelegramUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = TelegramUser.objects.order_by('id')
    serializer_class = TelegramUserSerializer
    filterset_class = TelegramUserFilterSet

    @extend_schema(responses=TelegramUserFavoriteSerializer(many=True),
                   filters=False,
                   summary='Get a list of Telegram user "Favorite cocktail" entities')
    @action(methods=['get'], detail=True)
    def favorites(self, request, *args, **kwargs):
        telegram_user = self.get_object()
        favorites = telegram_user.favorite_cocktails.select_related('cocktail').prefetch_related(
            'cocktail__categories',
            'cocktail__composition',
            'cocktail__composition__ingredient',
            'cocktail__composition__unit',
            'cocktail__recipe'
        ).order_by('-created_at')

        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = TelegramUserFavoriteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TelegramUserFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Favorite Cocktails'])
class FavoriteCocktailViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = FavoriteCocktail.objects.order_by('id')
    serializer_class = FavoriteCocktailSerializer
