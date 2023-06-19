from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUserManager(UserManager):
    """Кастомный менеджер для модели User."""

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField('username', null=True, max_length=100)
    email = models.EmailField('email', unique=True, max_length=250)
    question = models.CharField('question', max_length=100)
    answer = models.CharField(
        'answer', max_length=50, validators=[MinLengthValidator(1)])
    token = models.CharField('token', max_length=32)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['question', 'answer']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
