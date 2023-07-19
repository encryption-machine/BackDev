from django.core.exceptions import ValidationError

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

list_key_vigenere = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                     'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                     'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'a',
                     'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                     'x', 'y', 'z'
                     ]


def validate_key_caesar(value):
    ''' Валидация ключа для шифра Цезаря '''
    if value > 15:
        raise ValidationError('Слишком большой ключ')
    if value.isdigit() is False:
        raise ValidationError(f'{value} не является числом.')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validate_text_caesar(value):
    ''' Валидация ввода текста для шифра Цезаря '''
    if len(value) > 2000:
        raise ValidationError('Слишком большой текст')
    if value not in list_value_caesar:
        raise ValidationError(f'Вы ввели недопустимый символ {value}')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validate_text_morse(value):
    ''' Валидация шифра морзе '''
    if len(value) > 2000:
        raise ValidationError('Слишком большой текст')
    if value not in list_value_morse:
        raise ValidationError(f'Вы ввели недопустимый символ {value}')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validate_text_morse_decrypt(value):
    ''' Валидация ввода текста для дешифрования Морзе '''
    if len(value) > 15000:
        raise ValidationError('Слишком большой текст')
    if value not in ['-', ' ', '.']:
        raise ValidationError(f'Вы ввели недопустимый символ {value}')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validat_qr_vig_aes_text(value):
    ''' Валидация ввода текста qr, vigenere, aes '''
    if len(value) > 2000:
        raise ValidationError('Слишком большой текст')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validat_vig_aes_text_decrypt(value):
    ''' Валидация ввода дешифрования текста vigenere, aes '''
    if len(value) > 15000:
        raise ValidationError('Слишком большой текст')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validat_key_vigenere(value):
    ''' Валидация ключа для шифра vigenere '''
    if len(value) > 30:
        raise ValidationError('Слишком большой текст')
    if value not in list_key_vigenere:
        raise ValidationError(f'Вы ввели недопустимый символ {value}')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value


def validat_key_aes(value):
    ''' Валидация ключа для шифра aes '''
    if len(value) > 30:
        raise ValidationError('Слишком большой текст')
    if value == '':
        raise ValidationError('Вы не ввели ни одного символа.')
    return value
