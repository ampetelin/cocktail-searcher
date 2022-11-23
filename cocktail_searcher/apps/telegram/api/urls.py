from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.telegram.api.v1.urls'))
]
