from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomJWTCreateView, EncryptionListViewSet,
                    EncryptionViewSet, PasswordResetViewSet)

app_name = "api"

v1_router = DefaultRouter()
v1_router.register(
    "users/me/encryptions",
    EncryptionListViewSet,
    basename="encryption_history"
)
v1_router.register("encryption", EncryptionViewSet, basename="encryption")

v1_router.register("users", PasswordResetViewSet, basename="reset_password")

urlpatterns = [
    path("", include(v1_router.urls)),
    path("", include("djoser.urls")),
    path("auth/jwt/create/", CustomJWTCreateView.as_view(), name="jwt-create"),
    path("auth/", include("djoser.urls.jwt")),
]
