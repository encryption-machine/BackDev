"""
Django settings for encryption_machine project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY - 64@wl5gnrb!zhr88+%84#&s$3c0=q=8fiqtn*bc3unazh49oly
# SECRET_KEY = os.getenv('SECRET_KEY')
# SECRET_KEY = os.getenv("DJANGO_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_yasg",
    "djoser",
    "users",
    "encryption",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "encryption_machine.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "encryption_machine.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/api/.*$"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DJOSER = {
    'SERIALIZERS': {
        'user_create_password_retype': 'api.serializers.UserCreateSerializer',
    },
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "#/api/v1/users/password/reset/{uid}/{token}",
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAdminUser"],
        "user_list": ["rest_framework.permissions.IsAdminUser"],
        "activation": ["rest_framework.permissions.IsAdminUser"],
        "set_password": ["rest_framework.permissions.IsAdminUser"],
        "username_reset": ["rest_framework.permissions.IsAdminUser"],
        "username_reset_confirm": ["rest_framework.permissions.IsAdminUser"],
        "set_username": ["rest_framework.permissions.IsAdminUser"],
        "user_delete": ["rest_framework.permissions.IsAdminUser"],
    },
    "HIDE_USERS": False,
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
