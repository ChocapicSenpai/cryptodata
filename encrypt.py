from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
import os

def encrypt_file(file_path, key, salt):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=salt)
        with open(file_path, 'rb') as file:
            data = file.read()
        
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(salt + encrypted_data)

        print(f"Archivo encriptado como '{encrypted_file_path}'")
    except Exception as e:
        print(f"Error durante la encriptación: {e}")

if __name__ == "__main__":
    file_path = input("Ingrese la ruta del archivo a encriptar: ")
    while True:
        password = input("Ingrese la contraseña para encriptar (entre 12 y 30 caracteres): ")
        if 12 <= len(password) <= 30:
            break
        else:
            print("Error: La contraseña debe tener entre 12 y 30 caracteres.")

    salt = os.urandom(16)  # Generar un valor aleatorio para el salt
    key = PBKDF2(password.encode('utf-8'), salt, dkLen=16)  # Derivar una clave de 16 bytes a partir de la contraseña y el salt
    encrypt_file(file_path, key, salt)
