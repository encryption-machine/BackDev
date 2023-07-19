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

    # def encrypt_aes(self, text, key):
    #     try:
    #         validat_qr_vig_aes_text(text)
    #         validat_key_aes(key)
    #         return services.aes_encrypt(text, key)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def decrypt_aes(self, text, key):
    #     try:
    #         validat_vig_aes_text_decrypt(text)
    #         validat_key_aes(key)
    #         return services.aes_decrypt(text, key)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def encrypt_caesar(self, text, key):
    #     try:
    #         validate_text_caesar(text)
    #         validate_key_caesar(key)
    #         return services.encryption_mixin(text, key, is_encryption=True)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def decrypt_caesar(self, text, key):
    #     try:
    #         validate_text_caesar(text)
    #         validate_key_caesar(key)
    #         return services.encryption_mixin(text, key, is_encryption=False)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def encrypt_morse(self, text, *args):
    #     try:
    #         validate_text_morse(text)
    #         return services.morse_encode(text)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def decrypt_morse(self, text, *args):
    #     try:
    #         validate_text_morse_decrypt(text)
    #         return services.morse_decode(text)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def encrypt_qr(self, text, *args):
    #     try:
    #         validat_qr_vig_aes_text(text)
    #         return services.qr_code_generation(text)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def encrypt_vigenere(self, text, key):
    #     try:
    #         validat_qr_vig_aes_text(text)
    #         validat_key_vigenere(key)
    #         return services.vigenere_encode(text, key)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def decrypt_vigenere(self, text, key):
    #     try:
    #         validat_vig_aes_text_decrypt(text)
    #         validat_key_vigenere(key)
    #         return services.vigenere_decode(text, key)
    #     except ValueError:
    #         print('Неправильный ключ или текст')

    # def get_algorithm(self):
    #     encription_dict = {
    #         "aes": self.encrypt_aes,
    #         "caesar": self.encrypt_caesar,
    #         "morse": self.encrypt_morse,
    #         "qr": self.encrypt_qr,
    #         "vigenere": self.encrypt_vigenere,
    #     }

    #     decription_dict = {
    #         "aes": self.decrypt_aes,
    #         "caesar": self.decrypt_caesar,
    #         "morse": self.decrypt_morse,
    #         "vigenere": self.decrypt_vigenere,
    #     }
    #     if self.is_encryption:
    #         return encription_dict[self.algorithm](self.text, self.key)
    #     else:
    #         return decription_dict[self.algorithm](self.text, self.key)
