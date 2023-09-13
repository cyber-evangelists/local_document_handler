from cryptography.fernet import Fernet
import base64

secret_key = Fernet.generate_key()

fernet = Fernet(secret_key)

def encrypt_value(value):
    encrypted_value = fernet.encrypt(value.encode())
    encrypted_value_str = base64.urlsafe_b64encode(encrypted_value).decode()
    return encrypted_value_str

def decrypt_value(encrypted_value_str):
    encrypted_value = base64.urlsafe_b64decode(encrypted_value_str.encode())
    decrypted_value = fernet.decrypt(encrypted_value)
    return decrypted_value.decode()
