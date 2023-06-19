from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EncryptionViewSet

app_name = 'encryption'

router = DefaultRouter()

router.register('encryption', EncryptionViewSet, basename='encryption')


urlpatterns = [
    path('', include(router.urls)),
]
