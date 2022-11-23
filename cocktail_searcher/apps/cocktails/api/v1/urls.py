from rest_framework import routers

from apps.cocktails.api.v1 import views

router = routers.SimpleRouter()
router.register('cocktails', views.CocktailViewSet)

urlpatterns = router.urls
