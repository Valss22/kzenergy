import base64
import json
from cryptography.fernet import Fernet


def parse_id_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)


# def encrypting_password(password: str, enc_password=None) -> bytes:
#     key = Fernet.generate_key()
#     fernet = Fernet(key)
#     enc_password = fernet.encrypt(password.encode())
#     dec_password = fernet.decrypt(enc_password).decode()
#     return enc_password


# class CryptingPassword:
#     def __init__(self):
#         self.key = Fernet.generate_key()
#         self.fernet = Fernet(self.key)
#
#     def encode_password(self, password: str) -> bytes:
#         return self.fernet.encrypt(password.encode())
#
#     def decode_password(self, password: bytes) -> str:
#         return self.fernet.decrypt(password).decode()

