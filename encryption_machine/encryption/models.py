from django.db import models
from users.models import User


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
