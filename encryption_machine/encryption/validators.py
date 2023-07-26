from django.core.exceptions import ValidationError
from encryption.utils.aes import decrypt

ENCRYPTION_TEXT_LEN = 2000
DECRYPTION_TEXT_LEN = 15000
MAX_QR_TEXT_LEN = 1000
CAESAR_MAXIMUM_KEY = 15
MAX_KEY_LEN = 30

list_value_caesar = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                     'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                     'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 0,
                     1, 2, 3, 4, 5, 6, 7, 8, 9, ' ', '.', ',', '!', '"',
                     '#', '$', '%', '&', '(', ')', '*', '+', '-', '/', "'",
                     '~', '|', '}', '{', '[', ']', '=', '?', '_', '@', '<',
                     '>'
                     ]

list_value_morse = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                    'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                    'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 0,
                    1, 2, 3, 4, 5, 6, 7, 8, 9, ' ', '.', ',', '!', '"', '?',
                    '$', '%', '&', '(', ')', '*', '+', '-', '/', "'", '_',
                    ';', ':', '=', '@', '~', '|', '}', '{', '[', ']', '<',
                    '>', '#', '%', '*'
                    ]

list_vigenere = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' '
                 ]


def validate_caesar(text, key, is_encryption):
    '''Валидация шифра Цезаря '''
    if len(text) > ENCRYPTION_TEXT_LEN:
        raise ValidationError(
            f'Текст должен быть не более {ENCRYPTION_TEXT_LEN} символов.'
        )
    for char in text:
        if char.lower() not in list_value_caesar:
            raise ValidationError(f'Вы ввели недопустимый символ {char}')
    if not key:
        raise ValidationError('Необходимо ввести ключ')
    if key.isdigit() is False:
        raise ValidationError(f'{key} не является числом.')
    if int(key) > CAESAR_MAXIMUM_KEY:
        raise ValidationError(
            f'Ключ должен быть не больше {CAESAR_MAXIMUM_KEY}.')


def validate_morse(text, key, is_encryption):
    '''Валидация кода Морзе'''
    if is_encryption:
        if len(text) > ENCRYPTION_TEXT_LEN:
            raise ValidationError(
                f'Текст должен быть не более {ENCRYPTION_TEXT_LEN} символов.'
            )
    else:
        if len(text) > DECRYPTION_TEXT_LEN:
            raise ValidationError(
                f'Текст должен быть не более {DECRYPTION_TEXT_LEN} символов.'
            )
    if text == '':
        raise ValidationError('Вы не ввели ни одного символа.')


def validate_qr(text, key, is_encryption):
    """"Валидация QR-кода."""
    if not is_encryption:
        raise ValidationError('Доступно только шифрование')
    if len(text) > MAX_QR_TEXT_LEN:
        raise ValidationError(
            f'Текст должен быть не более {MAX_QR_TEXT_LEN} символов.'
        )
    if text == '':
        raise ValidationError('Вы не ввели ни одного символа.')


def validate_vigenere(text, key, is_encryption):
    """"Валидация шифра Виженера."""
    if len(text) > ENCRYPTION_TEXT_LEN:
        raise ValidationError(
            f'Текст должен быть не более {ENCRYPTION_TEXT_LEN} символов.'
        )
    if text == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    if not key:
        raise ValidationError('Необходимо ввести ключ')
    if len(key) > MAX_KEY_LEN:
        raise ValidationError(
            f'Ключ должен быть не более {MAX_KEY_LEN} символов.'
        )
    for char in text:
        if char.lower() not in list_vigenere:
            raise ValidationError(f'Вы ввели недопустимый символ {char}')
    for char in key:
        if char.lower() not in list_vigenere:
            raise ValidationError(
                f'Недопустимый символ {char}. Ключ должен быть словом')
    if key == '':
        raise ValidationError('Вы не ввели ни одного символа.')


def validate_aes(text, key, is_encryption):
    """"Валидация шифра AES."""
    if is_encryption:
        if len(text) > ENCRYPTION_TEXT_LEN:
            raise ValidationError(
                f'Текст должен быть не более {ENCRYPTION_TEXT_LEN} символов.'
            )
    else:
        if len(text) > DECRYPTION_TEXT_LEN:
            raise ValidationError(
                f'Текст должен быть не более {DECRYPTION_TEXT_LEN} символов.'
            )
    if text == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    if not key:
        raise ValidationError('Необходимо ввести ключ')
    if len(key) > MAX_KEY_LEN:
        raise ValidationError(
            f'Ключ должен быть не более {MAX_KEY_LEN} символов.'
        )
    if key == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    if not is_encryption:
        try:
            decrypt(text, key)
        except ValueError:
            raise ValidationError(
                'Некорректно закодированный текст, невозможно расшифровать.')
