import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

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

    messagebox.showinfo("Info", "Files renamed and copied successfully!")

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)

def start_renaming():
    input_directory = input_folder_entry.get().strip()
    prefix = prefix_entry.get().strip()
    output_directory = output_folder_entry.get().strip()

    if not input_directory or not prefix or not output_directory:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    # Buat directory tujuan jika belum ada
    os.makedirs(output_directory, exist_ok=True)

    # Panggil fungsi untuk merename dan menyalin file
    rename_files(input_directory, prefix, output_directory)

# Set up the main window
root = tk.Tk()
root.title("File Renamer")

# Create and place the widgets
tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Prefix:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
prefix_entry = tk.Entry(root, width=50)
prefix_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_output_folder).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Start", command=start_renaming).grid(row=3, column=0, columnspan=3, pady=10)

# Run the main loop
root.mainloop()
