import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def convert_password_to_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_password(password: str, cipher_suite: Fernet) -> str:
    encrypted_bytes = cipher_suite.encrypt(password.encode())
    return encrypted_bytes.decode('utf-8')



def decrypt_password(encrypted_password: str, cipher_suite: Fernet) -> str:

    decrypted_bytes = cipher_suite.decrypt(encrypted_password.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')