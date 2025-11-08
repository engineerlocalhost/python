import os
import shutil

# Folder utama tempat file-file berantakan berada
main_folder = "/home/hima/Pictures/latihan"

# Pemetaan ekstensi ke nama folder
file_types = {
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk", ".deb", ".rpm"],
    "Code": [".py", ".js", ".html", ".css", ".php", ".java", ".c", ".cpp"],
    "Others": []  # untuk ekstensi yang tidak dikenali
}

# Membuat folder tujuan jika belum ada
for folder in file_types.keys():
    os.makedirs(os.path.join(main_folder, folder), exist_ok=True)

# Fungsi untuk mendapatkan folder berdasarkan ekstensi
def get_folder_for_extension(ext):
    for folder, extensions in file_types.items():
        if ext.lower() in extensions:
            return folder
    return "Others"

# Memindahkan file ke folder yang sesuai
for filename in os.listdir(main_folder):
    file_path = os.path.join(main_folder, filename)
    
    if os.path.isfile(file_path):  # hanya file, bukan folder
        _, ext = os.path.splitext(filename)
        target_folder = get_folder_for_extension(ext)
        target_path = os.path.join(main_folder, target_folder, filename)

        try:
            shutil.move(file_path, target_path)
            print(f"✅ {filename} → {target_folder}/")
        except Exception as e:
            print(f"❌ Gagal memindahkan {filename}: {e}")

print("\nSelesai! Semua file telah diorganisir sesuai jenisnya.")
