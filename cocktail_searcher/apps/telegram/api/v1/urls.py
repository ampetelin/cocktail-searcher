from rest_framework import routers

from apps.telegram.api.v1 import views

router = routers.SimpleRouter()
router.register('telegram-users', views.TelegramUserViewSet)
router.register('favorites', views.FavoriteCocktailViewSet)

urlpatterns = router.urls
