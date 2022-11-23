from django.contrib import admin

from apps.telegram.models import TelegramUser, FavoriteCocktail


class FavoriteCocktailInline(admin.TabularInline):
    model = FavoriteCocktail
    readonly_fields = ('created_at',)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    inlines = [FavoriteCocktailInline]
