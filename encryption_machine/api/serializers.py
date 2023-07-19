from secrets import token_hex

from django.contrib.auth.password_validation import validate_password
from encryption.models import Encryption
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class CustomJWTCreateSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для создания jwt токена.

    Переопределяет текст ответа при ошибке."""

    default_error_messages = {
        "no_active_account": "Такой пользователь не зарегистирован"
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

    class Meta:
        model = Encryption
        fields = (
            "text", "algorithm", "key",
            "is_encryption", "encrypted_text", 'date')

    def get_encrypted_text(self, obj):
        return obj.get_algorithm()


class EncryptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода результата шфирования"""

    class Meta:
        model = Encryption
        fields = ("id", "text", "algorithm", "key", "is_encryption", "user")

    def validate_algorithm(self, value):
        if value not in ("aes", "caesar", "morse", "qr", "vigenere"):
            raise serializers.ValidationError(
                "Шифр содержит неправильное название")

        return value

    def create(self, validated_data):
        user = self.context.get("request").user
        if user.is_authenticated:
            encryption = Encryption.objects.create(user=user, **validated_data)
        else:
            encryption = Encryption.objects.create(**validated_data)
        return encryption

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj_1 = Encryption.objects.get(id=obj["id"])
        encrypted_text = obj_1.get_algorithm()
        return {"encrypted_text": encrypted_text}
