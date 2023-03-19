import os
from cryptography.fernet import Fernet

def encrypt(string_value):
  key = os.getenv("CRYPTO_KEY")
  fernet = Fernet(key)
  return fernet.encrypt(string_value.encode())