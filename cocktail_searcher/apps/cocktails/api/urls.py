from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.cocktails.api.v1.urls'))
]
