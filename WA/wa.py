from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess

# Fungsi untuk menyambungkan ke VPN
def connect_to_vpn():
    print("Menyambungkan ke VPN...")
    subprocess.run(["protonvpn-cli", "connect", "--cc", "SG"])  # Ganti "ID" dengan kode negara yang diinginkan
    time.sleep(10)  # Tunggu hingga VPN terhubung

# Fungsi untuk memutuskan VPN
def disconnect_vpn():
    print("Memutuskan VPN...")
    subprocess.run(["protonvpn-cli", "disconnect"])

# Fungsi untuk membuat email
def create_gmail_account(first_name, last_name, phone_number, index):
    # Inisialisasi WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Menghindari deteksi otomatisasi
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://accounts.google.com/signup")

    # Tunggu hingga halaman dimuat
    time.sleep(5)

    # Isi formulir pembuatan akun
    first_name_field = driver.find_element(By.NAME, "firstName")
    first_name_field.send_keys(first_name)

    last_name_field = driver.find_element(By.NAME, "lastName")
    last_name_field.send_keys(last_name)

    next_button = driver.find_element(By.XPATH, '//*[@id="collectNameNext"]/div/button')
    next_button.click()

    time.sleep(2)

    # Pilih bulan, hari, dan tahun
    month_field = driver.find_element(By.XPATH, '//*[@id="month"]')
    month_field.send_keys("Januari")

    day_field = driver.find_element(By.XPATH, '//*[@id="day"]')
    day_field.send_keys("01")

    year_field = driver.find_element(By.XPATH, '//*[@id="year"]')
    year_field.send_keys("1990")

    gender_field = driver.find_element(By.XPATH, '//*[@id="gender"]/option[3]')
    gender_field.click()

    next_button = driver.find_element(By.XPATH, '//*[@id="birthdaygenderNext"]/div/button')
    next_button.click()

    time.sleep(2)

    # Pilih "Gunakan alamat email saya saat ini"
    use_current_email = driver.find_element(By.XPATH, '//*[@id="selectionc2"]')
    use_current_email.click()

    next_button = driver.find_element(By.XPATH, '//*[@id="next"]/div/button')
    next_button.click()

    time.sleep(2)

    # Masukkan nomor telepon
    phone_field = driver.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
    phone_field.send_keys(phone_number)

    next_button = driver.find_element(By.XPATH, '//*[@id="next"]/div/button')
    next_button.click()

    time.sleep(2)

    # Verifikasi nomor telepon (Anda perlu menangani verifikasi manual atau menggunakan layanan SMS)
    # Di sini kita hanya menunggu input manual
    input("Silakan verifikasi nomor telepon dan tekan Enter untuk melanjutkan...")

    # Simpan informasi email ke file
    email = f"{first_name}.{last_name}_{index:04d}@gmail.com"
    with open("emails.txt", "a") as file:
        file.write(f"{email}\n")

    driver.quit()

# Main program
first_name = "SJM"
last_name = "Medeia"
phone_number = "6281188826874"

# Sambungkan ke VPN sebelum membuat akun
connect_to_vpn()

try:
    for i in range(1, 6):
        create_gmail_account(first_name, last_name, phone_number, i)
        print(f"Email {i} berhasil dibuat.")
finally:
    # Putuskan VPN setelah selesai
    disconnect_vpn()