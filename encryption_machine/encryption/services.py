from .utils import (aes, caesar_code, morse_code, qr_code,
                    vigenere)
from django.core.exceptions import ValidationError

from .validators import validate_aes, validate_caesar, validate_morse, validate_qr, validate_vigenere


class EncryptionService:
    """Класс хранения логики шифрования."""

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

    def get_algorithm(self, algorithm, text, key, is_encryption):
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
        
        if is_encryption:
            return encription_dict[algorithm](text, key)
        else:
            return decription_dict[algorithm](text, key)

    def get_validator(self, algorithm, text, key, is_encryption):
        validation_dict = {
            "aes": validate_aes,
            "caesar": validate_caesar,
            "morse": validate_morse,
            "qr": validate_qr,
            "vigenere": validate_vigenere,
        }
        try:
            validation_dict[algorithm](text, key, is_encryption)
        except ValidationError:
            raise

