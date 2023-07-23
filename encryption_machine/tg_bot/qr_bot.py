import base64

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton

async def handle_qr_code_cipher(cipher_functions, cipher, text, message, state):
    try:
        cipher_function = cipher_functions.get(cipher)
        result = cipher_function(text)
        photo_bytes = base64.b64decode(result)
        await message.reply_photo(photo_bytes)
        await state.finish()
        await message.answer("Для нового шифрования нажмите /start")
    except Exception:
        await state.finish()
        await message.answer("Бот упал. Ауч. Для нового шифрования нажмите /start")