from cryptography.fernet import Fernet
import os

# Fungsi untuk memuat kunci dari file
def load_key(key_path):
    return open(key_path, "rb").read()

# Fungsi untuk mendekripsi file
def decrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(filename[:-4], 'wb') as file:
        file.write(decrypted_data)
    os.remove(filename)

# Fungsi untuk mendekripsi semua file dalam folder
def decrypt_folder(folder_path, key_path):
    key = load_key(key_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.enc'):
            file_path = os.path.join(folder_path, filename)
            decrypt_file(file_path, key)

if __name__ == "__main__":
    # Meminta input file kunci dari pengguna
    key_path = input("Masukkan path file kunci: ")
    
    if not os.path.isfile(key_path):
        print("File kunci tidak ditemukan.")
        exit()

    # Ganti 'your_folder_path' dengan path folder Anda
    folder_path = 'Masukan path target'
    decrypt_folder(folder_path, key_path)
    print("Folder berhasil didekripsi.")
