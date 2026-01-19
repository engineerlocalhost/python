import webbrowser
import pandas as pd
import time
import re
import pyautogui
import pyperclip

file_excel = "/home/captennem0/Documents/DevopsProject/python/WhatsappBulkInterview/kandidat.xlsx"
df = pd.read_excel(file_excel)

template_pesan = """Yth. Saudara/i {nama},

Dengan hormat,

Sehubungan dengan proses seleksi yang sedang berlangsung, kami mengundang Saudara/i untuk mengikuti sesi interview pada posisi:

{posisi}

Adapun detail pelaksanaan interview adalah sebagai berikut:
Hari/Tanggal : Rabu, 21 Januari 2026
Waktu        : 10.00 WIB
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


for index, row in df.iterrows():
    nama = row["nama_kandidat"]
    posisi = row["posisi"]
    raw_number = row["no_wa"]

    no_wa = normalize_number(raw_number)

    if no_wa is None:
        print(f"❌ Nomor tidak valid: {nama} ({raw_number})")
        continue

    pesan = template_pesan.format(nama=nama, posisi=posisi)

    print(f"📤 Mengirim ke {nama} ({no_wa})...")

    try:
        url = f"https://web.whatsapp.com/send?phone={no_wa.replace('+','')}"
        webbrowser.open(url)

        time.sleep(10)  # tunggu WhatsApp Web buka

        pyperclip.copy(pesan)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")  # SEND otomatis

        print("✅ Terkirim. Tunggu 3 detik...\n")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Gagal kirim ke {nama}: {e}")
        continue
