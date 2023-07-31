from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os

def unpad(data):
    return data[:-data[-1]]

def decrypt_file(file_path, key, salt):
    try:
        with open(file_path, 'rb') as encrypted_file:
            data = encrypted_file.read()

        cipher = AES.new(key, AES.MODE_CBC, iv=salt)
        decrypted_data = cipher.decrypt(data)
        unpadded_data = unpad(decrypted_data)

        decrypted_file_path = file_path.replace(".enc", "_decrypted.docx")
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(unpadded_data)

        print(f"Archivo desencriptado como '{decrypted_file_path}'")
    except Exception as e:
        print(f"Error durante la desencriptación: {e}")

        

if __name__ == "__main__":
    file_path = input("Ingrese la ruta del archivo encriptado: ")
    password = input("Ingrese la contraseña para desencriptar (entre 12 y 30 caracteres): ")

    # Leer el salt almacenado en el archivo encriptado
    with open(file_path, 'rb') as encrypted_file:
        salt = encrypted_file.read(16)  # El salt tiene 16 bytes (mismo tamaño que la clave derivada)

    # Derivar la clave a partir de la contraseña y el salt
    key = PBKDF2(password.encode('utf-8'), salt, dkLen=16)

    decrypt_file(file_path, key, salt)

    # if verify_key(file_path, key):
    #     decrypt_file(file_path, key, salt)
    # else:
    #     print("Error: La contraseña es incorrecta.")