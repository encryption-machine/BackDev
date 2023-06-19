from secrets import token_hex

from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User


class ResetPasswordReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',  'question')


class ResetPasswordWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ResetPasswordReadSerializer(
            instance=instance, context=context).data


class ResetPasswordQuestionReadSerializer(serializers.ModelSerializer):
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
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id',  'answer')

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
    new_password = serializers.CharField(
        required=True, write_only=True, min_length=8)
    re_new_password = serializers.CharField(
        required=True, write_only=True, min_length=8)
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id',  'token', 're_new_password', 'new_password')

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
