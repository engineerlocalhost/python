import webbrowser
import pandas as pd
import time
import re
import pyautogui
import pyperclip
import random
import os
from datetime import datetime

file_excel = "/home/captennem0/Documents/DevopsProject/python/WhatsappBulkInterview/kandidat2.xlsx"
log_file = "log_wa.csv"

df = pd.read_excel(file_excel)

template_pesan = """Yth. Saudara/i {nama},

Dengan hormat,

Sehubungan dengan proses seleksi yang sedang berlangsung, kami mengundang Saudara/i untuk mengikuti sesi interview pada posisi:

{posisi}

Adapun detail pelaksanaan interview adalah sebagai berikut:
Hari/Tanggal : Rabu, 21 Januari 2026
Waktu        : {jam} WIB
Lokasi       : Rukan Puri Mutiara Blok BD21, Sunter, Jakarta Utara

Mohon Saudara/i untuk membawa CV dan portofolio terbaru sebagai bahan pendukung saat interview.

Catatan:
Mohon untuk mengonfirmasi kehadiran Saudara/i dengan membalas chat ini atau menghubungi kami paling lambat 1 hari sebelum jadwal interview.

Hormat kami,
Tim Rekrutmen
PT. Sumber Jaya Music (Arctic Hunter Indonesia)
"""

def normalize_number(number):
    num = str(number).strip().replace(" ", "").replace("-", "")

    if num.startswith("08"):
        num = "+62" + num[1:]
    elif num.startswith("628"):
        num = "+" + num
    elif num.startswith("+628"):
        pass
    else:
        return None

    if not re.match(r"^\+628[0-9]{7,12}$", num):
        return None

    return num

# Load log jika ada (resume mode)
sent_numbers = set()
if os.path.exists(log_file):
    log_df = pd.read_csv(log_file)
    sent_numbers = set(log_df[log_df["status"] == "SUKSES"]["no_wa"].astype(str))

def save_log(nama, no_wa, status, error=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = pd.DataFrame([[nama, no_wa, status, now, error]],
                       columns=["nama", "no_wa", "status", "waktu", "error"])
    if os.path.exists(log_file):
        row.to_csv(log_file, mode="a", header=False, index=False)
    else:
        row.to_csv(log_file, index=False)

print("📲 Membuka WhatsApp Web...")
webbrowser.open("https://web.whatsapp.com")
time.sleep(25)

for index, row in df.iterrows():
    nama = row["nama_kandidat"]
    posisi = row["posisi"]
    jam = str(row["jam"]).strip()
    raw_number = row["no_wa"]

    no_wa = normalize_number(raw_number)

    if no_wa is None:
        print(f"❌ Nomor tidak valid: {nama} ({raw_number})")
        save_log(nama, raw_number, "GAGAL", "Nomor tidak valid")
        continue

    if no_wa in sent_numbers:
        print(f"⏭️ Skip (sudah terkirim): {nama}")
        continue

    pesan = template_pesan.format(
        nama=nama,
        posisi=posisi,
        jam=jam
    )

    print(f"📤 Mengirim ke {nama} ({no_wa})...")

    try:
        url = f"https://web.whatsapp.com/send?phone={no_wa.replace('+','')}"
        webbrowser.open(url)

        time.sleep(12)

        pyperclip.copy(pesan)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")

        print("✅ Terkirim")

        save_log(nama, no_wa, "SUKSES")

        delay = random.randint(20, 30)
        print(f"⏳ Delay {delay} detik...\n")
        time.sleep(delay)

    except Exception as e:
        print(f"❌ Gagal kirim ke {nama}: {e}")
        save_log(nama, no_wa, "GAGAL", str(e))
        continue

print("🎉 Semua pesan selesai diproses.")
