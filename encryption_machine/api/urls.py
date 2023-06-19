from django.urls import include, path

from .views import (reset_password, reset_password_confirm,
                    reset_password_question)

app_name = 'api'

urlpatterns = [
    path('users/reset_password/', reset_password, name='reset_password'),
    path('users/reset_password_question/', reset_password_question, name='reset_password_question'),
    path('users/reset_password_confirm/', reset_password_confirm, name='reset_password_confirm'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
