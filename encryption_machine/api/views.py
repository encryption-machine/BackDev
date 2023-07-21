from secrets import token_hex

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from encryption.models import Encryption
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from .serializers import (EncryptionReadSerializer, EncryptionSerializer,
                          ResetPasswordConfirmSerializer,
                          ResetPasswordQuestionReadSerializer,
                          ResetPasswordQuestionWriteSerializer,
                          ResetPasswordReadSerializer,
                          ResetPasswordWriteSerializer)


class CustomJWTCreateView(TokenObtainPairView):
    """Кастомный вьюсет для создания jwt токена."""

    _serializer_class = "api.serializers.CustomJWTCreateSerializer"


class PasswordResetViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == "reset_password":
            return ResetPasswordWriteSerializer
        if self.action == "reset_password_question":
            return ResetPasswordQuestionWriteSerializer
        return ResetPasswordConfirmSerializer

    @swagger_auto_schema(
        methods=["POST"],
        request_body=ResetPasswordWriteSerializer,
        responses={
            status.HTTP_200_OK: ResetPasswordReadSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"field_name": openapi.Schema(type="string")},
            ),
        },
    )
    @action(methods=["post"], detail=False)
    def reset_password(self, request):
        """Запрос на восстановление пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data["email"]
        context = {"request": request}
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=ResetPasswordQuestionWriteSerializer,
        responses={
            status.HTTP_200_OK: ResetPasswordQuestionReadSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"field_name": openapi.Schema(type="string")},
            ),
        },
    )
    @action(methods=["post"], detail=False)
    def reset_password_question(self, request):
        """Ответа на секретный вопрос при восстановлении пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.data["id"]
        context = {"request": request}
        user = get_object_or_404(User, id=id)
        serializer = self.get_serializer(
            user, context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=ResetPasswordConfirmSerializer,
        responses={
            status.HTTP_201_CREATED: "Password changed successfully",
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"field_name": openapi.Schema(type="string")},
            ),
        },
    )
    @action(methods=["post"], detail=False)
    def reset_password_confirm(self, request):
        """Обновления пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.data["id"]
        user = get_object_or_404(User, id=id)
        user.set_password(request.data["new_password"])
        token = token_hex(16)
        user.token = token
        user.save()
        return Response(
            {"Пароль успешно изменен"}, status=status.HTTP_201_CREATED)


class EncryptionListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для истории шифрований."""

    serializer_class = EncryptionReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Encryption.objects.filter(user=self.request.user.id)


class EncryptionViewSet(viewsets.ModelViewSet):
    """Вьюсет для шифрования"""

    queryset = Encryption.objects.all()
    serializer_class = EncryptionSerializer
    http_method_names = ["post"]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            encryption = Encryption.objects.create(user=user, **serializer.validated_data)

