from secrets import token_hex

from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from encryption.models import Encryption
from rest_framework import serializers
from users.models import User


class ResetPasswordReadSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на запрос на восстановление пароля."""

    class Meta:
        model = User
        fields = ('id', 'question')


class ResetPasswordWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса на восстановление пароля."""

    class Meta:
        model = User
        fields = ('email',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ResetPasswordReadSerializer(
            instance=instance, context=context).data


class ResetPasswordQuestionReadSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа после успешного вода ответа на вопрос."""

    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'token')

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
        fields = ('id', 'answer')

    def validate_answer(self, value):
        user = get_object_or_404(
            User, id=self.context.get('request').data['id'])
        if value != user.answer:
            raise serializers.ValidationError(
                'Wrong answer to security question')
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ResetPasswordQuestionReadSerializer(
            instance=instance, context=context).data


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    """Сериализатор для смены пароля на новый."""

    new_password = serializers.CharField(
        required=True, write_only=True, min_length=8)
    re_new_password = serializers.CharField(
        required=True, write_only=True, min_length=8)
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'token', 're_new_password', 'new_password')

    def validate_token(self, value):
        user = get_object_or_404(
            User, id=self.context.get('request').data['id'])
        if value != user.token:
            raise serializers.ValidationError(
                'Invalid password recovery token')
        return value

    def validate_new_password(self, value):
        if value != self.context.get('request').data['re_new_password']:
            raise serializers.ValidationError(
                'Password mismatch')
        validate_password(value)
        return value


class EncryptionReadSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса к истории шифрований."""

    encrypted_text = serializers.SerializerMethodField()

    class Meta:
        model = Encryption
        fields = (
            'text', 'algorithm', 'key', 'is_encryption', 'encrypted_text', 'data')

    def get_encrypted_text(self, obj):
        return obj.get_algorithm()


class EncryptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода результата шфирования"""

    class Meta:
        model = Encryption
        fields = (
            'id',
            'text',
            'algorithm',
            'key',
            'is_encryption',
            'user'
        )

    def validate_algorithm(self, value):
        if value not in ('aes', 'caesar', 'morse', 'qr', 'vigenere'):
            raise serializers.ValidationError("Шрифт содержит неправильное название")
        return value

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.is_authenticated:
            encryption = Encryption.objects.create(user=user, **validated_data)
        else:
            encryption = Encryption.objects.create(**validated_data)
        return encryption
    
    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj_1 = Encryption.objects.get(id=obj['id'])
        encrypted_text = obj_1.get_algorithm()
        return {'encrypted_text': encrypted_text}
    