from . import services
import base64
from io import BytesIO
import qrcode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from django.core.exceptions import PermissionDenied

NOT_DEFINED_LANG = "nd"

MORSE_DICT = {
    "А": ".-",
    "Б": "-...",
    "В": ".--",
    "Г": "--.",
    "Д": "-..",
    "Е": ".",
    "Ж": "...-",
    "З": "--..",
    "И": "..",
    "Й": ".---",
    "К": "-.-",
    "Л": ".-..",
    "М": "--",
    "Н": "-.",
    "О": "---",
    "П": ".--.",
    "Р": ".-.",
    "С": "...",
    "Т": "-",
    "У": "..-",
    "Ф": "..-.",
    "Х": "....",
    "Ц": "-.-.",
    "Ч": "---.",
    "Ш": "----",
    "Щ": "--.-",
    "Ъ": "--.--",
    "Ы": "-.--",
    "Ь": "-..-",
    "Э": "..-..",
    "Ю": "..--",
    "Я": ".-.-",
    " ": " ",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    ";": "-.-.-.",
    "(": "-.--.",
    ")": "-.--.-",
    "?": "..--..",
    "!": "-.-.--",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "/": "-..-.",
    "$": "...-..-",
    "@": ".--.-.",
    "&": ".-...",
    "¡": "--...-",
    "_": "..--.-",
    '"': ".-..-.",
    "¿": "..-.-",
    "'": ".----.",
}

MORSE_DICT_REVERSED = {value: key for key, value in MORSE_DICT.items()}


def aes_encrypt(text, key):
    text = text.encode("utf-8")
    key = key.encode("utf-8")
    key = SHA256.new(key).digest()
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(text) % AES.block_size
    text += bytes([padding]) * padding
    data = iv + encryptor.encrypt(text)
    return base64.b64encode(data).decode("latin-1")


def aes_decrypt(text, key):
    key = key.encode("utf-8")
    text = base64.b64decode(text.encode("latin-1"))
    key = SHA256.new(key).digest()
    iv = text[: AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    data = decryptor.decrypt(text[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding].decode("utf-8")


def encryption_mixin(text, key, is_encryption):
    final_string = ""
    for symbol in text:
        if symbol.isupper():
            symbol_index = ord(symbol) + ord("А")
            if is_encryption:
                symbol_position = (symbol_index + key) % 32 + ord("А")
            else:
                symbol_position = (symbol_index - key) % 32 + ord("А")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        elif symbol.islower():
            symbol_index = ord(symbol) - ord("а")
            if is_encryption:
                symbol_position = (symbol_index + key) % 32 + ord("а")
            else:
                symbol_position = (symbol_index - key) % 32 + ord("а")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        elif symbol.isdigit():
            # если это число, сдвиньте его фактическое значение
            if is_encryption:
                symbol_index = (int(symbol) + key) % 10
            else:
                symbol_index = (int(symbol) - key) % 10
            final_string += str(symbol_index)
        elif ord(symbol) >= 32 and ord(symbol) <= 47:
            # если это число,4 сдвинуть его фактическое значение
            symbol_index = ord(symbol) - ord(" ")
            if is_encryption:
                symbol_position = (symbol_index + key) % 15 + ord(" ")
            else:
                symbol_position = (symbol_index - key) % 15 + ord(" ")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        else:
            # если нет ни алфавита, ни числа, оставьте все как есть
            final_string += symbol
    return final_string


def morse_encode(text):
    splited_text = [[i for i in word] for word in text.split()]
    return "  ".join(
        [
            " ".join([MORSE_DICT.get(letter.upper(), "?") for letter in word])
            for word in splited_text
        ]
    )


def morse_decode(text):
    encoded_words = text.split("  ")
    return " ".join(["".join(
        [MORSE_DICT_REVERSED.get(i, "?") for i in word.split()]).lower()
        for word in encoded_words]
    )


"""
Выбрана эта библиотека, как самая популярная
https://pypi.org/project/qrcode/
"""


def qr_code_generation(text: str) -> str:
    """ Создание QR-кода на основе заданного текста """
    img = qrcode.make(text)
    # Создание буфера для сохранения изображения
    buffered = BytesIO()
    # Сохранение изображения в буфер
    img.save(buffered)
    # Преобразование изображения в строку base64
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


"""
При переходе по qr коду у пользователя открывается страница браузера, далее:
1)если зашифрована url, то открывается страница
2)если текст, то происходит запрос по этому тексту в поисковике
"""


def vigenere_codec(text: str, key: str, codec: int = 1):
    """
    Код Виженера.
    Для повышения устойчивости все слова переводятся в верхний регистр,
    Цифры и знаки не шифруются. Исходный текст желательно вводить без пробелов.
    В фунцию передается текст для шифровки/дешифровки,
    ключ шифрования,
    опционально: параметр codec для определения
    направления шифрования (1 - шифровка(умолч.)/ -1 - дешифровка),
    """

    result = ""
    key = key.upper()
    # Словарь алфавитов.
    # название_языка : [код_первого_символа, длина_алфавита]
    lang_dict = {"en": [64, 26], "ru": [1039, 32]}

    # Определяем язык ключа. Язык по умолчанию NOT_DEFINED_LANG
    lang = NOT_DEFINED_LANG
    for letter in key:
        for lang_test, [lang_start, lang_len] in lang_dict.items():
            if 0 <= (ord(letter) - lang_start) <= lang_len:
                lang = lang_test
                break
        if lang != NOT_DEFINED_LANG:
            break

    # Если язык неизвестен, то текст возвращается в исходном виде.
    if lang == NOT_DEFINED_LANG:
        return text

    # код первой буквы алфавита
    zero_letter = lang_dict[lang][0]
    # длина алфавита
    alphabet_length = lang_dict[lang][1]

    # Очищаем ключ от символов, не принадлежащих алфавиту
    new_key = ""
    for letter in key:
        if zero_letter < ord(letter) < zero_letter + alphabet_length:
            new_key += letter

    # Шифрование предполагает сдвиг кода буквы на число,
    # соответствующее коду соответствующей буквы ключа.
    i = 0
    for letter in text.upper():
        if zero_letter < ord(letter) < zero_letter + alphabet_length:
            result += chr(
                (ord(new_key[i]) * codec - 1 + ord(letter) - 2 * zero_letter)
                % alphabet_length
                + zero_letter
            )
            i = i + 1 if i < len(new_key) - 1 else 0
        else:
            result += letter
    return result


def vigenere_encode(text: str, key: str):
    return vigenere_codec(text, key, 1)


def vigenere_decode(text: str, key: str):
    return vigenere_codec(text, key, -1)
