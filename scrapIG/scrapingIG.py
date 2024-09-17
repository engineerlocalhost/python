import instaloader
import time
import random
import csv
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from datetime import datetime

# Fungsi login dan simpan session
def login_and_save_session(username, password, session_path):
    L = instaloader.Instaloader()
    try:
        L.login(username, password)  # Login ke Instagram
        L.save_session_to_file(session_path)  # Simpan session ke file
        print(f"Session cookies untuk akun {username} telah tersimpan.")
        return True
    except Exception as e:
        print(f"Login gagal: {e}")
        return False

# Fungsi untuk memuat session dan scrape profil
def scrape_profile_using_session(username, session_path, target_profile, start_date, end_date):
    L = instaloader.Instaloader()
    try:
        L.load_session_from_file(username, session_path)  # Muat session
        profile = instaloader.Profile.from_username(L.context, target_profile)
        print(f"Profil {profile.username} berhasil diambil.")
        print(f"Jumlah pengikut: {profile.followers}")

        # Mengunduh foto dan video dari profil
        data = []
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        for post in profile.get_posts():
            if start_date <= post.date_utc <= end_date:
                media_type = "Photo" if not post.is_video else "Video"
                caption = post.caption if post.caption else "No caption"
                date = post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Men-download post dengan caption: {caption[:50]}")
                L.download_post(post, target=profile.username)
                data.append([date, caption, media_type])
            elif post.date_utc < start_date:
                break

        print("Semua media telah diunduh.")
        return data
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

# Fungsi untuk memilih file session
def select_session_file():
    root = Tk()
    root.withdraw()  # Sembunyikan jendela utama
    file_path = filedialog.asksaveasfilename(defaultextension=".session",
                                           filetypes=[("Session files", "*.session"), ("All files", "*.*")])
    root.destroy()
    return file_path

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Caption", "Media Type"])
            writer.writerows(data)
        print(f"Data berhasil disimpan ke {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke CSV: {e}")

# GUI untuk pengaturan
def gui():
    def on_login_button_click():
        username = entry_username.get()
        password = entry_password.get()
        session_path = select_session_file()  # Pilih lokasi penyimpanan session

        if not session_path:
            messagebox.showerror("Error", "Lokasi penyimpanan session tidak dipilih.")
            return

        if login_and_save_session(username, password, session_path):
            messagebox.showinfo("Success", "Login berhasil dan session disimpan!")
        else:
            messagebox.showerror("Error", "Login gagal. Cek username dan password.")

    def on_scrape_button_click():
        username = entry_username.get()
        session_path = select_session_file()  # Pilih file session untuk memuat
        target_profile = entry_target_profile.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        
        if not session_path:
            messagebox.showerror("Error", "File session tidak dipilih.")
            return

        if not start_date or not end_date:
            messagebox.showerror("Error", "Rentang tanggal tidak lengkap.")
            return

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Format tanggal salah. Gunakan YYYY-MM-DD.")
            return

        data = scrape_profile_using_session(username, session_path, target_profile, start_date, end_date)
        if data:
            csv_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if csv_path:
                save_to_csv(data, csv_path)
                messagebox.showinfo("Success", "Scraping dan penyimpanan CSV berhasil!")
            else:
                messagebox.showerror("Error", "Lokasi penyimpanan CSV tidak dipilih.")
        else:
            messagebox.showerror("Error", "Scraping gagal.")

    # Setup GUI
    root = Tk()
    root.title("Instagram Scraper")

    Label(root, text="Username:").pack()
    entry_username = Entry(root)
    entry_username.pack()

    Label(root, text="Password:").pack()
    entry_password = Entry(root, show="*")
    entry_password.pack()

    Label(root, text="Target Profile:").pack()
    entry_target_profile = Entry(root)
    entry_target_profile.pack()

    Label(root, text="Start Date (YYYY-MM-DD):").pack()
    entry_start_date = Entry(root)
    entry_start_date.pack()

    Label(root, text="End Date (YYYY-MM-DD):").pack()
    entry_end_date = Entry(root)
    entry_end_date.pack()

    Button(root, text="Login and Save Session", command=on_login_button_click).pack()
    Button(root, text="Scrape Profile", command=on_scrape_button_click).pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
