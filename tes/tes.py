import sqlite3
from tkinter import *
from tkinter import messagebox

# Membuat koneksi ke database SQLite
conn = sqlite3.connect('barang_keluar.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS barang_keluar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_surat TEXT,
        divisi TEXT,
        tanggal TEXT,
        perihal TEXT,
        nama_artis TEXT,
        sosmed TEXT,
        alamat TEXT,
        no_faktur TEXT,
        nama_barang TEXT,
        qty INTEGER
    )
''')
conn.commit()

# Fungsi untuk menyimpan data ke database
def simpan_data():
    no_surat = entry_no_surat.get()
    divisi = entry_divisi.get()
    tanggal = entry_tanggal.get()
    perihal = entry_perihal.get()
    nama_artis = entry_nama_artis.get()
    sosmed = entry_sosmed.get()
    alamat = entry_alamat.get()
    no_faktur = entry_no_faktur.get()
    nama_barang = entry_nama_barang.get()
    qty = entry_qty.get()
    
    if no_surat and divisi and tanggal and nama_artis and qty:
        cursor.execute('''
            INSERT INTO barang_keluar (no_surat, divisi, tanggal, perihal, nama_artis, sosmed, alamat, no_faktur, nama_barang, qty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (no_surat, divisi, tanggal, perihal, nama_artis, sosmed, alamat, no_faktur, nama_barang, qty))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil disimpan")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Semua kolom wajib diisi!")

# Fungsi untuk menghapus data input setelah disimpan
def clear_entries():
    entry_no_surat.delete(0, END)
    entry_divisi.delete(0, END)
    entry_tanggal.delete(0, END)
    entry_perihal.delete(0, END)
    entry_nama_artis.delete(0, END)
    entry_sosmed.delete(0, END)
    entry_alamat.delete(0, END)
    entry_no_faktur.delete(0, END)
    entry_nama_barang.delete(0, END)
    entry_qty.delete(0, END)

# Membuat GUI dengan Tkinter
root = Tk()
root.title("Aplikasi Pencatatan Barang Keluar")

# Label dan Entry untuk setiap field
Label(root, text="No Surat").grid(row=0, column=0, padx=10, pady=5)
entry_no_surat = Entry(root)
entry_no_surat.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Divisi").grid(row=1, column=0, padx=10, pady=5)
entry_divisi = Entry(root)
entry_divisi.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Tanggal").grid(row=2, column=0, padx=10, pady=5)
entry_tanggal = Entry(root)
entry_tanggal.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Perihal").grid(row=3, column=0, padx=10, pady=5)
entry_perihal = Entry(root)
entry_perihal.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Nama Artis").grid(row=4, column=0, padx=10, pady=5)
entry_nama_artis = Entry(root)
entry_nama_artis.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Sosmed").grid(row=5, column=0, padx=10, pady=5)
entry_sosmed = Entry(root)
entry_sosmed.grid(row=5, column=1, padx=10, pady=5)

Label(root, text="Alamat").grid(row=6, column=0, padx=10, pady=5)
entry_alamat = Entry(root)
entry_alamat.grid(row=6, column=1, padx=10, pady=5)

Label(root, text="No Faktur").grid(row=7, column=0, padx=10, pady=5)
entry_no_faktur = Entry(root)
entry_no_faktur.grid(row=7, column=1, padx=10, pady=5)

Label(root, text="Nama Barang").grid(row=8, column=0, padx=10, pady=5)
entry_nama_barang = Entry(root)
entry_nama_barang.grid(row=8, column=1, padx=10, pady=5)

Label(root, text="QTY").grid(row=9, column=0, padx=10, pady=5)
entry_qty = Entry(root)
entry_qty.grid(row=9, column=1, padx=10, pady=5)

# Tombol untuk menyimpan data
btn_simpan = Button(root, text="Simpan", command=simpan_data)
btn_simpan.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()

# Menutup koneksi database saat aplikasi ditutup
conn.close()
