from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, filters


class TelegramUserFilterSet(FilterSet):
    chat_id = filters.NumberFilter(help_text=_('Telegram user chat identifier'))
