from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User

from .serializers import (ResetPasswordConfirmSerializer,
                          ResetPasswordQuestionReadSerializer,
                          ResetPasswordQuestionWriteSerializer,
                          ResetPasswordReadSerializer,
                          ResetPasswordWriteSerializer)


@swagger_auto_schema(
    methods=['POST'],
    request_body=ResetPasswordWriteSerializer,
    responses={
        status.HTTP_200_OK: ResetPasswordReadSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"field_name": openapi.Schema(type="string")})})
@api_view(['POST'])
def reset_password(request):
    """Запроса на восстановление пароля."""
    if 'email' not in request.data.keys():
        return Response(
            {'email': ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    context = {'request': request}
    if not User.objects.filter(email=email).exists():
        return Response(
            {'email': ['User with this email does not exist']},
            status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, email=email)
    return Response(
        ResetPasswordWriteSerializer(user, context=context).data,
        status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['POST'],
    request_body=ResetPasswordQuestionWriteSerializer,
    responses={
        status.HTTP_200_OK: ResetPasswordQuestionReadSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"field_name": openapi.Schema(type="string")})})
@api_view(['POST'])
def reset_password_question(request):
    """Ответа на секретный вопрос при восстановлении пароля."""
    if 'id' not in request.data.keys():
        return Response(
            {'id': ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST)
    if 'answer' not in request.data.keys():
        return Response(
            {'answer': ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST)
    id = request.data['id']
    context = {'request': request}
    user = get_object_or_404(User, id=id)
    serializer = ResetPasswordQuestionWriteSerializer(
        user, context=context, data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['POST'],
    request_body=ResetPasswordConfirmSerializer,
    responses={
        status.HTTP_204_NO_CONTENT: 'Password changed successfully',
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"field_name": openapi.Schema(type="string")})})
@api_view(['POST'])
def reset_password_confirm(request):
    """Обновления пароля."""
    if 'id' not in request.data.keys():
        return Response(
            {'id': ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST)
    id = request.data['id']
    if not User.objects.filter(id=id).exists():
        return Response(
            {'id': ['User with this id does not exist']},
            status=status.HTTP_400_BAD_REQUEST)
    context = {'request': request}
    user = get_object_or_404(User, id=id)
    serializer = ResetPasswordConfirmSerializer(
        user, context=context, data=request.data)
    serializer.is_valid(raise_exception=True)
    user.set_password(request.data['new_password'])
    user.save()
    return Response(
        {'Пароль успешно изменен'}, status=status.HTTP_204_NO_CONTENT)
