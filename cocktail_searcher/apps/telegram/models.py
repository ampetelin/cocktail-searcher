from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.cocktails.models import Cocktail


class TelegramUser(models.Model):
    chat_id = models.PositiveBigIntegerField(unique=True, verbose_name=_('Chat ID'))

    class Meta:
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')

    def __str__(self):
        return str(self.chat_id)


class FavoriteCocktail(models.Model):
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name='favorite_cocktails', verbose_name=_('Telegram user')
    )
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, verbose_name=_('Cocktail'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date added to favorites'))

    class Meta:
        verbose_name = _('Favorite cocktail')
        verbose_name_plural = _('Favorite cocktails')
        constraints = [
            models.UniqueConstraint(fields=('telegram_user', 'cocktail'), name='%(app_label)s_%(class)s_cpk')
        ]
