from secrets import token_hex

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreatePasswordRetypeSerializer
from encryption.models import Encryption
from encryption.services import EncryptionService
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    def to_representation(self, instance):
        token_class = RefreshToken
        refresh = token_class.for_user(instance)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class CustomJWTCreateSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для создания jwt токена.

    Переопределяет текст ответа при ошибке."""

    default_error_messages = {
        "no_active_account": "Неправильное имя пользователя или пароль"
    }


class ResetPasswordReadSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на запрос на восстановление пароля."""

    class Meta:
        model = User
        fields = ("id", "question")


class ResetPasswordWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса на восстановление пароля."""

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email",)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist")
        return value

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return ResetPasswordReadSerializer(
            instance=instance, context=context).data


class ResetPasswordQuestionReadSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа после успешного вода ответа на вопрос."""

    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "token")

    def get_token(self, obj):
        token = token_hex(16)
        obj.token = token
        obj.save()
        return token


class ResetPasswordQuestionWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для ввода ответа на секретный вопрос."""

    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("id", "answer")

    def validate(self, data):
        if not User.objects.filter(id=data["id"]).exists():
            raise serializers.ValidationError(
                "Пользователя с таким id не существует")
        user = User.objects.get(id=data["id"])
        if data["answer"] != user.answer:
            raise serializers.ValidationError(
                "Неверный ответ на секретный вопрос")
        return data

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return ResetPasswordQuestionReadSerializer(
            instance=instance, context=context
        ).data


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    """Сериализатор для смены пароля на новый."""

    new_password = serializers.CharField(
        required=True, write_only=True, min_length=8)
    re_new_password = serializers.CharField(
        required=True, write_only=True, min_length=8
    )
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("id", "token", "re_new_password", "new_password")

    def validate(self, data):
        if not User.objects.filter(id=data["id"]).exists():
            raise serializers.ValidationError(
                "Пользователя с таким id не существует")
        user = User.objects.get(id=data["id"])
        if data["token"] != user.token:
            raise serializers.ValidationError(
                "Неверный токен восстановления пароля")
        return data

    def validate_new_password(self, value):
        if value != self.context.get("request").data["re_new_password"]:
            raise serializers.ValidationError("Password mismatch")
        validate_password(value)
        return value


class EncryptionReadSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса к истории шифрований."""

    encrypted_text = serializers.SerializerMethodField()
    encryption_service = EncryptionService()

    class Meta:
        model = Encryption
        fields = (
            "text", "algorithm", "key",
            "is_encryption", "encrypted_text", "date"
        )

    def get_encrypted_text(self, obj):
        encrypted_text = self.encryption_service.get_algorithm(
            obj.algorithm, obj.text, obj.key, obj.is_encryption
        )
        return encrypted_text


class EncryptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода результата шфирования"""

    encryption_service = EncryptionService()
    key = serializers.CharField(required=False)

    class Meta:
        model = Encryption
        fields = ("id", "text", "algorithm", "key", "is_encryption")

    def to_internal_value(self, data):
        if data.get('algorithm') in ('morse', 'qr'):
            if data.get('key') is not None:
                data.pop('key')
        return super(EncryptionSerializer, self).to_internal_value(data)

    def validate_algorithm(self, value):
        if value not in ("aes", "caesar", "morse", "qr", "vigenere"):
            raise serializers.ValidationError(
                "Шифр содержит неправильное название")
        return value

    def validate(self, data):
        text = data["text"]
        key = data.get("key", None)
        is_encryption = data["is_encryption"]
        algorithm = data["algorithm"]
        try:
            self.encryption_service.get_validator(
                algorithm, text, key, is_encryption)
        except ValidationError as error:
            raise serializers.ValidationError(error.message)
        return data

    def to_representation(self, instance):
        algorithm = self.context.get("request").data["algorithm"]
        text = str(self.context.get("request").data["text"])
        key = str(self.context.get("request").data.get("key", None))
        is_encryption = self.context.get("request").data["is_encryption"]

        encrypted_text = self.encryption_service.get_algorithm(
            algorithm, text, key, is_encryption
        )
        return {"encrypted_text": encrypted_text}
