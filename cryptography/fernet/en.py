from cryptography.fernet import Fernet
import os

# Tentukan path untuk file kunci
KEY_PATH = 'path/a.key'

# Fungsi untuk menghasilkan kunci
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

# Fungsi untuk memuat kunci dari file
def load_key():
    return open(KEY_PATH, "rb").read()

# Fungsi untuk mengenkripsi file
def encrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(filename + '.enc', 'wb') as file:
        file.write(encrypted_data)
    os.remove(filename)

# Fungsi untuk mengenkripsi semua file dalam folder
def encrypt_folder(folder_path):
    key = load_key()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

if __name__ == "__main__":
    # Buat kunci jika belum ada
    if not os.path.isfile(KEY_PATH):
        generate_key()

    # Tentukan path folder yang ingin dienkripsi
    folder_path = 'path target'
    encrypt_folder(folder_path)
    print("Folder berhasil dienkripsi.")
