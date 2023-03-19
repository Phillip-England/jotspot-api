import os
from cryptography.fernet import Fernet

def decrypt(encoded_value):
  key = os.getenv("CRYPTO_KEY")
  fernet = Fernet(key)
  return fernet.decrypt(encoded_value).decode()