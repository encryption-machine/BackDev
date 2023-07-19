from django.db import models
from users.models import User

from .encryption_algorithms import (aes, caesar_code, morse_code, qr_code,
                                    vigenere)


class Encryption(models.Model):
    """Модель шифрования."""

    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="encryptions"
    )
    text = models.TextField(max_length=2000)
    algorithm = models.CharField(max_length=100)
    key = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_encryption = models.BooleanField()  # True - шифруем, False - дешифруем

    class Meta:
        verbose_name = "Шифрование"
        verbose_name_plural = "Шифрования"

    def encrypt_aes(self, text, key):
        return aes.encrypt(text, key)

    def decrypt_aes(self, text, key):
        return aes.decrypt(text, key)

    def encrypt_caesar(self, text, key):
        return caesar_code.encryption_mixin(text, key, is_encryption=True)

    def decrypt_caesar(self, text, key):
        return caesar_code.encryption_mixin(text, key, is_encryption=False)

    def encrypt_morse(self, text, *args):
        return morse_code.encode(text)

    def decrypt_morse(self, text, *args):
        return morse_code.decode(text)

    def encrypt_qr(self, text, *args):
        return qr_code.qr_code_generation(text)

    def encrypt_vigenere(self, text, key):
        return vigenere.encode(text, key)

    def decrypt_vigenere(self, text, key):
        return vigenere.decode(text, key)

    def get_algorithm(self):
        encription_dict = {
            "aes": self.encrypt_aes,
            "caesar": self.encrypt_caesar,
            "morse": self.encrypt_morse,
            "qr": self.encrypt_qr,
            "vigenere": self.encrypt_vigenere,
        }

        decription_dict = {
            "aes": self.decrypt_aes,
            "caesar": self.decrypt_caesar,
            "morse": self.decrypt_morse,
            "vigenere": self.decrypt_vigenere,
        }
        if self.is_encryption:
            return encription_dict[self.algorithm](self.text, self.key)
        else:
            return decription_dict[self.algorithm](self.text, self.key)
