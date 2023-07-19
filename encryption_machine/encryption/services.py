from django.db import models
from .utils import (aes, caesar_code, morse_code, qr_code,
                    vigenere)

from .validations import (validate_key_caesar, validate_text_caesar,
                          validate_text_morse, validat_qr_vig_aes_text,
                          validat_vig_aes_text_decrypt, validat_key_aes,
                          validate_text_morse_decrypt,
                          validat_key_vigenere)


class EncryptionService(models.Model):
    """Модель шифрования."""

    def encrypt_aes(self, text, key):
        try:
            validat_qr_vig_aes_text(text)
            validat_key_aes(key)
            return aes.encrypt(text, key)
        except ValueError:
            print('Неправильный ключ или текст')

    def decrypt_aes(self, text, key):
        try:
            validat_vig_aes_text_decrypt(text)
            validat_key_aes(key)
            return aes.decrypt(text, key)
        except ValueError:
            print('Неправильный ключ или текст')

    def encrypt_caesar(self, text, key):
        try:
            validate_text_caesar(text)
            validate_key_caesar(key)
            return caesar_code.encryption_mixin(text, key, is_encryption=True)
        except ValueError:
            print('Неправильный ключ или текст')

    def decrypt_caesar(self, text, key):
        try:
            validate_text_caesar(text)
            validate_key_caesar(key)
            return caesar_code.encryption_mixin(text, key, is_encryption=False)
        except ValueError:
            print('Неправильный ключ или текст')

    def encrypt_morse(self, text, *args):
        try:
            validate_text_morse(text)
            return morse_code.encode(text)
        except ValueError:
            print('Неправильный ключ или текст')

    def decrypt_morse(self, text, *args):
        try:
            validate_text_morse_decrypt(text)
            return morse_code.decode(text)
        except ValueError:
            print('Неправильный ключ или текст')

    def encrypt_qr(self, text, *args):
        try:
            validat_qr_vig_aes_text(text)
            return qr_code.qr_code_generation(text)
        except ValueError:
            print('Неправильный ключ или текст')

    def encrypt_vigenere(self, text, key):
        try:
            validat_qr_vig_aes_text(text)
            validat_key_vigenere(key)
            return vigenere.encode(text, key)
        except ValueError:
            print('Неправильный ключ или текст')

    def decrypt_vigenere(self, text, key):
        try:
            validat_vig_aes_text_decrypt(text)
            validat_key_vigenere(key)
            return vigenere.decode(text, key)
        except ValueError:
            print('Неправильный ключ или текст')

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
