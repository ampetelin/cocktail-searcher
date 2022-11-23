from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.cocktails.api.v1.serializers import CocktailSerializer
from apps.telegram.models import TelegramUser, FavoriteCocktail


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = (
            'id',
            'chat_id'
        )


class FavoriteCocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCocktail
        fields = (
            'id',
            'telegram_user',
            'cocktail',
            'created_at',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteCocktail.objects.all(),
                fields=('telegram_user', 'cocktail')
            )
        ]


class TelegramUserFavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cocktail = CocktailSerializer()
    created_at = serializers.DateTimeField()
