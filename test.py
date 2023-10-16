from cryptography.fernet import Fernet

# Generate a key for encryption (keep this secret)
key = Fernet.generate_key()
print("Key String: ", key)

# Initialize the Fernet cipher
cipher_suite = Fernet(key)

# Your string to encrypt
plaintext = "Kanye West"

# Convert the string to bytes
plaintext_bytes = plaintext.encode('utf-8')

# Encrypt the bytes
cipher_text = cipher_suite.encrypt(plaintext_bytes)

# Print the encrypted text
print("Encrypted String:", cipher_text.decode('utf-8'))

# To decrypt, you'll need the same key:
decrypted_bytes = cipher_suite.decrypt(cipher_text)
decrypted_text = decrypted_bytes.decode('utf-8')
print("Decrypted String:", decrypted_text)
