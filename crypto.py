import sqlite3

import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


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

class KeyStorage:
    def __init__ (self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.public_key = self.private_key.public.key()

        
    def set_public_key(self, public_key):
        self.public_key = public_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key
    
    def print_keys(self):
        print("Private Key:")
        print(self.private_key)
        print("\nPublic Key:")
        print(self.public_key)