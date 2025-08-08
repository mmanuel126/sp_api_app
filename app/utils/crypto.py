# app/utils/crypto.py

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import os
from dotenv import load_dotenv

load_dotenv()

IV = bytes([0x12, 0x34, 0x56, 0x78, 0x90, 0xab, 0xcd, 0xef])
KEY = os.getenv("ENCRYPTION_KEY", "").encode("utf-8")

def encrypt(text: str) -> str:
    try:
        cipher = DES.new(KEY, DES.MODE_CBC, IV)
        padded_text = pad(text.encode("utf-8"), DES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode("utf-8")
    except Exception as e:
        return ""

def decrypt(cipher_text: str) -> str:
    try:
        cipher_text = cipher_text.replace(" ", "+")
        encrypted = base64.b64decode(cipher_text)
        cipher = DES.new(KEY, DES.MODE_CBC, IV)
        decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)
        return decrypted.decode("utf-8")
    except Exception:
        return ""