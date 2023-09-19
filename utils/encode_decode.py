import base64
from settings import AES_KEY
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_string(plaintext):
    key = AES_KEY
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    encoded_ciphertext = base64.b64encode(ciphertext).decode()
    return encoded_ciphertext


def decrypt_string(encoded_ciphertext):
    key = AES_KEY
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = base64.b64decode(encoded_ciphertext)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size).decode()
    return plaintext

