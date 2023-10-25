from cryptography.fernet import Fernet
from services.logs import logger
import base64

secret_key = Fernet.generate_key()
# secret_key = b'ZZjV1ciRBYOJSuvuKWCqePUQSRYokb0T3BWqR35hSys='
fernet = Fernet(secret_key)

def encrypt_value(value):
    encrypted_value = fernet.encrypt(value.encode())
    encrypted_value_str = base64.urlsafe_b64encode(encrypted_value).decode()
    return encrypted_value_str

def decrypt_value(encrypted_value_str):
    try:
        encrypted_value = base64.urlsafe_b64decode(encrypted_value_str.encode())
        decrypted_value = fernet.decrypt(encrypted_value)
        return decrypted_value.decode()
    except:
        return False

if __name__ == '__main__':
    # print(encrypt_value('admin'))
    print(decrypt_value('Z0FBQUFBQmxPTTdIT2xOU0xSeE1qSGRpajM4REFScjE5ektLZ0l1Yk92RGU0WG9lOUhPb3I3NTBvQm5EX3ZzazdIQnhyMW1sN3FlNzVVS0ZjZnUzSkdyVlJoTnJYeGZUamc9PQ=='))
