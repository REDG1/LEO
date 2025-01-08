from cryptography.fernet import Fernet
from django.conf import settings
from hashlib import sha256
from base64 import urlsafe_b64encode

def generate_fernet_key(secret_key):
    # Generate a 32-byte key using SHA-256 hash of the Django SECRET_KEY
    key = sha256(secret_key.encode()).digest()
    # Encode the key to make it URL-safe
    encoded_key = urlsafe_b64encode(key)
    return encoded_key

def encrypt_parameter(parameter):
    key = generate_fernet_key(settings.SECRET_KEY)  # Use Django's secret key as the encryption key
    cipher_suite = Fernet(key)
    encrypted_parameter = cipher_suite.encrypt(parameter.encode())
    return encrypted_parameter

def decrypt_parameter(encrypted_parameter):
    key = generate_fernet_key(settings.SECRET_KEY)  # Use Django's secret key as the encryption key
    cipher_suite = Fernet(key)
    encrypted_parameter = encrypted_parameter.decode()
    decrypted_parameter = cipher_suite.decrypt(encrypted_parameter).decode()
    return decrypted_parameter