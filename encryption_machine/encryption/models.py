from django.db import models
from users.models import User

from .encryption_algorithms import aes, morse_code


class Encryption(models.Model):
    """Модель шифрования."""
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='encryptions')
    text = models.TextField(max_length=2000)
    encryption_algorithm = models.CharField(max_length=100)
    key = models.CharField(max_length=100, null=True)
    is_encryption = models.BooleanField()  # True - шифруем, False - дешифруем

    class Meta:
        verbose_name = 'Шифрование'
        verbose_name_plural = 'Шифрования'

    def encrypt_aes(text, key):
        return aes.encrypt(text, key)

    def decrypt_aes(text, key):
        return aes.decrypt(text, key)

    def encrypt_caesar(text, key):
        pass

    def decrypt_caesar(text, key):
        pass

    def encrypt_dsa(text, key):
        pass

    def decrypt_dsa(text, key):
        pass

    def encrypt_morse(text):
        return morse_code.encode(text)

    def decrypt_morse(text):
        return morse_code.decode(text)

    def encrypt_qr(text):
        pass

    def decrypt_qr(text):
        pass

    def encrypt_vigenere(text, key):
        pass

    def decrypt_vigenere(text, key):
        pass
