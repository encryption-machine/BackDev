import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(text, key):
    key = SHA256.new(key).digest()
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(text) % AES.block_size
    text += bytes([padding]) * padding
    data = IV + encryptor.encrypt(text)
    return base64.b64encode(data).decode("latin-1")


def decrypt(text, key):
    text = base64.b64decode(text.encode("latin-1"))
    key = SHA256.new(key).digest()
    IV = text[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(text[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding].decode('utf-8')
