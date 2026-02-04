import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# ================== KONFIGURASI ==================

FILE_TYPES = {
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk", ".deb", ".rpm"],
    "Code": [".py", ".js", ".html", ".css", ".php", ".java", ".c", ".cpp"],
    "Others": []
}

# ================== HELPER ==================

def get_folder_by_extension(ext):
    for folder, exts in FILE_TYPES.items():
        if ext.lower() in exts:
            return folder
    return "Others"

def find_last_number(path, prefix):
    max_n = 0
    pattern = re.compile(re.escape(prefix) + r"(\d+)")
    if not os.path.exists(path):
        return 0

    for f in os.listdir(path):
        match = pattern.search(f)
        if match:
            max_n = max(max_n, int(match.group(1)))
    return max_n

# ================== GUI ACTION ==================

def browse_source():
    p = filedialog.askdirectory()
    if p:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, p)

def browse_dest():
    p = filedialog.askdirectory()
    if p:
        dest_entry.delete(0, tk.END)
        dest_entry.insert(0, p)

def organize_files():
    source = source_entry.get()
    dest = dest_entry.get()
    pattern = rename_entry.get().strip()
    mode = numbering_mode.get()

    if not source or not dest:
        messagebox.showerror("Error", "Source dan Destination harus diisi")
        return

    if pattern and "{n}" not in pattern:
        messagebox.showwarning(
            "Peringatan",
            "Rename pattern sebaiknya mengandung {n}"
        )

    # Buat folder tujuan
    for folder in FILE_TYPES:
        os.makedirs(os.path.join(dest, folder), exist_ok=True)

    counters = {}

    # Inisialisasi counter awal
    if pattern:
        base_prefix = pattern.replace("{n}", "")
        if mode == "global":
            counters["global"] = find_last_number(dest, base_prefix)

        else:
            for folder in FILE_TYPES:
                folder_path = os.path.join(dest, folder)
                counters[folder] = find_last_number(folder_path, base_prefix)

    for file in os.listdir(source):
        src_path = os.path.join(source, file)
        if not os.path.isfile(src_path):
            continue

        name, ext = os.path.splitext(file)
        folder = get_folder_by_extension(ext)
        target_dir = os.path.join(dest, folder)

        key = "global" if mode == "global" else folder
        counters.setdefault(key, 0)
        counters[key] += 1

        if pattern:
            new_name = pattern.format(
                n=counters[key],
                type=folder,
                ext=ext.replace(".", "")
            ) + ext
        else:
            new_name = file

        # ===== ANTI OVERWRITE =====
        final_path = os.path.join(target_dir, new_name)
        base, ext2 = os.path.splitext(new_name)
        i = 1
        while os.path.exists(final_path):
            final_path = os.path.join(target_dir, f"{base}_{i}{ext2}")
            i += 1

        shutil.move(src_path, final_path)

    messagebox.showinfo("Sukses", "🎉 File berhasil diorganisir!")

# ================== GUI ==================

root = tk.Tk()
root.title("File Organizer PRO")
root.geometry("560x380")
root.resizable(False, False)

tk.Label(root, text="Source Folder").pack(anchor="w", padx=10)
source_entry = tk.Entry(root, width=65)
source_entry.pack(padx=10)
tk.Button(root, text="Browse", command=browse_source).pack(pady=4)

tk.Label(root, text="Destination Folder").pack(anchor="w", padx=10)
dest_entry = tk.Entry(root, width=65)
dest_entry.pack(padx=10)
tk.Button(root, text="Browse", command=browse_dest).pack(pady=4)

tk.Label(root, text="Rename Pattern (contoh: HM__{n})").pack(anchor="w", padx=10)
rename_entry = tk.Entry(root, width=65)
rename_entry.pack(padx=10)

# Mode numbering
numbering_mode = tk.StringVar(value="global")

tk.Label(root, text="Mode Penomoran").pack(anchor="w", padx=10, pady=5)
tk.Radiobutton(root, text="🔢 Global", variable=numbering_mode, value="global").pack(anchor="w", padx=30)
tk.Radiobutton(root, text="📂 Per Kategori", variable=numbering_mode, value="category").pack(anchor="w", padx=30)

tk.Button(
    root,
    text="🚀 Organize Files",
    command=organize_files,
    bg="#4CAF50",
    fg="white",
    height=2
).pack(pady=15)

root.mainloop()
