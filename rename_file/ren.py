import os
import shutil

def rename_files(input_directory, prefix, output_directory):
    # Dapatkan daftar file di direktori input
    files = os.listdir(input_directory)
    
    # Filter hanya file, bukan folder
    files = [f for f in files if os.path.isfile(os.path.join(input_directory, f))]
    
    # Urutkan file
    files.sort()
    
    # Rename dan salin file ke output_directory
    for index, file_name in enumerate(files, start=1):
        # Dapatkan ekstensi file
        file_ext = os.path.splitext(file_name)[1]
        # Buat nama file baru dengan prefix
        new_name = f"{prefix}-{index:02d}{file_ext}"  # 02d untuk nomor urutan dua digit
        # Dapatkan path lengkap untuk file lama dan baru
        old_path = os.path.join(input_directory, file_name)
        new_path = os.path.join(output_directory, new_name)
        # Salin dan rename file ke direktori output
        shutil.copy2(old_path, new_path)
        print(f"Copied and renamed: {file_name} to {new_name}")

# Minta input dari user
input_directory = input("Masukkan path directory sumber: ")
prefix = input("Masukkan prefix yang diinginkan untuk nama file: ")
output_directory = input("Masukkan path directory tujuan: ")

# Buat directory tujuan jika belum ada
os.makedirs(output_directory, exist_ok=True)

# Panggil fungsi untuk merename dan menyalin file
rename_files(input_directory, prefix, output_directory)
