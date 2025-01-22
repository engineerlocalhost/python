import pyautogui
import time

def send_whatsapp_message_via_desktop(message):
    try:
        # Fokuskan aplikasi WhatsApp Desktop (pastikan aplikasi sudah terbuka)
        print("Arahkan ke jendela WhatsApp Desktop dalam 5 detik...")
        time.sleep(5)  # Memberi waktu untuk mengarahkan ke jendela WhatsApp Desktop

        # Ketik pesan
        pyautogui.typewrite(message)
        pyautogui.press('enter')
        print("Pesan terkirim.")
    except Exception as e:
        print(f"Gagal mengirim pesan: {e}")

if __name__ == "__main__":
    # Nomor tujuan (dalam konteks WhatsApp Desktop, nomor tujuan harus sudah dipilih di aplikasi)
    target_number = "+6281315992477"
    print(f"Mengirim pesan ke {target_number}")

    # Pesan yang akan dikirim
    message = "Hallo sayangku"

    # Kirim pesan setiap 2 detik
    while True:
        send_whatsapp_message_via_desktop(message)
        time.sleep(2)
