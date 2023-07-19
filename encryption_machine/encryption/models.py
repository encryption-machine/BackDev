from django.db import models
from users.models import User
from . import services
from .validations import (validate_key_caesar, validate_text_caesar,
                          validate_text_morse, validat_qr_vig_aes_text,
                          validat_vig_aes_text_decrypt, validat_key_aes,
                          validate_text_morse_decrypt,
                          validat_key_vigenere)


class Encryption(models.Model):
    """Модель шифрования."""

    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="encryptions"
    )
    text = models.TextField(max_length=2000)
    algorithm = models.CharField(max_length=100)
    key = models.CharField(max_length=100, null=True)
    is_encryption = models.BooleanField()  # True - шифруем, False - дешифруем

    class Meta:
        verbose_name = "Шифрование"
        verbose_name_plural = "Шифрования"
