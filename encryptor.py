from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

BLOCK_SIZE = 16  # AES block size
KEY_SIZE = 32    # 256-bit key

def pad(data):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding]) * padding

def unpad(data):
    return data[:-data[-1]]

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000)

def encrypt_file(file_path, password):
    salt = get_random_bytes(16)
    key = derive_key(password.encode(), salt)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext))

    encrypted_file = file_path + ".enc"
    with open(encrypted_file, 'wb') as f:
        f.write(salt + iv + ciphertext)

    print(f"[+] File encrypted successfully: {encrypted_file}")

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()

    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext))

    decrypted_file = file_path.replace(".enc", ".dec")
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted)
    
    print(f"[+] File decrypted successfully: {decrypted_file}")

def main():
    print("=== AES-256 File Encryption Tool ===")
    print("1. Encrypt File")
    print("2. Decrypt File")
    choice = input("Choose an option: ")

    if choice not in ['1', '2']:
        print("Invalid option")
        return

    file_path = input("Enter path to file: ")
    if not os.path.isfile(file_path):
        print("File not found!")
        return

    password = input("Enter password: ")

    if choice == '1':
        encrypt_file(file_path, password)
    else:
        decrypt_file(file_path, password)

if __name__ == "__main__":
    main()
