from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Konfigurasi Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")

# Path ke ChromeDriver
service = Service('D:/Kampus/UT/_Pemrogramman/python/delmess/chromedriver.exe')  # Ganti dengan path ke ChromeDriver Anda
driver = webdriver.Chrome(service=service, options=chrome_options)

# Masukkan URL Facebook Messenger
driver.get('https://www.messenger.com')

# Tunggu beberapa detik agar halaman sepenuhnya dimuat
time.sleep(5)

# Masukkan email dan password Facebook Anda
email = 'dcukay@gmail.com'
password = 'Sayasaja007'

# Temukan elemen untuk email dan password, lalu masukkan data
driver.find_element(By.NAME, 'email').send_keys(email)
driver.find_element(By.NAME, 'pass').send_keys(password)
driver.find_element(By.NAME, 'pass').send_keys(Keys.RETURN)

# Tunggu hingga login selesai
time.sleep(10)

# Temukan chat yang ingin dihapus
# Ganti dengan nama chat atau ID chat yang sesuai
chat_name = 'Nama Chat'

# Klik pada chat
chat = driver.find_element(By.XPATH, f"//span[text()='{chat_name}']")
chat.click()

# Tunggu beberapa detik agar chat terbuka
time.sleep(5)

# Klik pada tombol menu
menu_button = driver.find_element(By.XPATH, "//div[@aria-label='More actions']")
menu_button.click()

# Klik pada opsi hapus
delete_option = driver.find_element(By.XPATH, "//span[text()='Delete Chat']")
delete_option.click()

# Konfirmasi penghapusan
confirm_button = driver.find_element(By.XPATH, "//span[text()='Delete']")
confirm_button.click()

# Tunggu beberapa detik agar penghapusan selesai
time.sleep(5)

# Tutup browser
driver.quit()
