from django.db import models
from .utils import (aes, caesar_code, morse_code, qr_code,
                    vigenere)

from .validations import (validate_key_caesar, validate_text_caesar_morse,
                          validat_qr_vig_aes_text, validat_key_aes,
                          validat_vig_aes_text_decrypt,
                          validate_text_morse_decrypt,
                          validat_key_vigenere)


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

    def get_algorithm(self, text, key, is_encryption):
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
            return encription_dict[self.algorithm](text, key)
        else:
            return decription_dict[self.algorithm](text, key)

    def get_validations(self, key, text, is_encryption, algorithm):
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
            if algorithm == encription_dict['aes']:
                if encription_dict['aes'](keyvalidat_qr_vig_aes_text(text), validat_key_aes(key)):
                    return True
                else:
                    return False
            if algorithm == encription_dict['caesar']:
                if encription_dict['caesar'](validate_text_caesar(text), validate_key_caesar(key)):
                    return True
                else:
                    return False
            if algorithm == encription_dict['morse']:
                if encription_dict['morse'](validate_text_morse(text)):
                    return True
                else:
                    return False
            if algorithm == encription_dict['qr']:
                if algorithm == encription_dict['qr'](validat_qr_vig_aes_text(text)):
                    return True
                else:
                    return False
            if algorithm == encription_dict['vigenere']:
                if encription_dict['vigenere'](validat_qr_vig_aes_text(text), validat_key_vigenere(key)):
                    return True
                else:
                    return False
        else:
            if algorithm == decription_dict['aes']:
                if decription_dict['aes'](validat_vig_aes_text_decrypt(text), validat_key_aes(key)):
                    return True
                else:
                    return False
            if algorithm == decription_dict['caesar']:
                if decription_dict['caesar'](validate_text_caesar(text), validate_key_caesar(key)):
                                        return True
                else:
                    return False
            if algorithm == decription_dict['morse']:
                if decription_dict['morse'](validate_text_morse_decrypt(text)):
                    return True
                else:
                    return False
            if algorithm == decription_dict['vigenere']:
                if decription_dict['vigenere'](validat_vig_aes_text_decrypt(text), validat_key_vigenere(key)):
                    return True
                else:
                    return False
