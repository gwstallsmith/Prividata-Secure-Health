import sqlite3

import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


# Function hash ALL PASSWORDS in database
def salt_passwords():
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Username, Password FROM Credentials")
        result = cursor.fetchall()

        for user in result:
            salted_password = hash_password(user[1])
            cursor.execute("UPDATE Credentials SET Password = ? WHERE Username = ?", (salted_password, user[0]))


# Function to get the result of hashing a password
def hash_password(password):
    # Encode for hashing to work
    password = password.encode('utf-8')

    hash = hashlib.sha256()         # Create Hashing object
    hash.update(password)           # Apply hashing algorithm
    hash_pass = hash.hexdigest()    # Use hex representation

    return hash_pass


class AES:
    def __init__(self, password):
        self.kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'salt',
                    iterations=100000,
                    backend=default_backend()
                )
        self.shared_secret = base64.urlsafe_b64encode(self.kdf.derive(password))

    def aes_encrypt(self, message):
        key = self.shared_secret
        fernet = Fernet(key)
        encrypted = fernet.encrypt(message.encode())
        return encrypted

    # Function to decrypt using AES
    def aes_decrypt(self, encrypted):
        key = self.shared_secret
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)
        return decrypted.decode()
    
    def print(self):
        print("Shared Secret: ")
        print(self.shared_secret)
