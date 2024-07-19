import pywhatkit as kit
import pandas as pd
import time
import os

# Path ke file Excel
file_path = r"D:\Kampus\UT\_Pemrogramman\python\bulkWA\data.xlsx"

# Periksa apakah file ada
if not os.path.exists(file_path):
    print(f"File tidak ditemukan: {file_path}")
else:
    # Baca data dari file Excel
    data = pd.read_excel(file_path)

    # Loop melalui setiap baris dalam data
    for index, row in data.iterrows():
        nama = row["Nama"]
        posisi = row["Position"]
        phone = row["Phone"]
        text = row["Text"]

        # Format pesan WhatsApp
        message = f"Selamat Malam Ka {nama}\n\nKami dari xxxxxx mengundang Anda untuk mengikuti proses interview untuk posisi {posisi} yang akan dilaksanakan pada:\n\nHari/Tanggal: xxxx, xxx xx 2024\nWaktu: Pukul 11:00 WIB\nLokasi: xxxxxxx\n\nMohon konfirmasi kehadiran Anda melalui pesan ini. Jika ada pertanyaan atau membutuhkan informasi lebih lanjut, jangan ragu untuk menghubungi kami.\n\nTerima kasih dan sampai jumpa!\n\nSalam,\nManager HRD\nPT. XXXXX"

        # Kirim pesan WhatsApp secara instan
        kit.sendwhatmsg_instantly(f"+{phone}", message, 15, tab_close=False)

        # Tunggu beberapa detik sebelum mengirim pesan berikutnya
        time.sleep(30)
