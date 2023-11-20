import sqlite3

import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

import os

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


def generate_shared_secret(password, salt=b'MySalt', iterations=100000, length=32):
    backend = default_backend()

    # Derive a key from the password using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=backend
    )

    # Generate the shared secret
    shared_secret = kdf.derive(password.encode())

    # Convert the shared secret to base64-encoded bytes
    encoded_secret = base64.urlsafe_b64encode(shared_secret)

    # Store the encoded shared secret in the environment variable
    os.environ["SHARED_SECRET"] = encoded_secret.decode()

    return encoded_secret

def encrypt(data):
    cipher_suite = Fernet(os.environ["SHARED_SECRET"].encode('utf-8'))
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data

def decrypt(encrypted_data):
    cipher_suite = Fernet(os.environ["SHARED_SECRET"].encode('utf-8'))
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data
