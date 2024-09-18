from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox

# Fungsi untuk mencari gambar di Pinterest
def search_pinterest(query, num_images, save_folder):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Operasikan di background
    
    # Setup WebDriver
    service = Service('path/to/chromedriver')  # Ganti dengan path ke WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Kunjungi Pinterest dan cari gambar
    search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    driver.get(search_url)
    
    # Tunggu halaman sepenuhnya dimuat
    driver.implicitly_wait(10)  # Tunggu hingga elemen yang diperlukan dimuat
    
    image_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
    
    if not image_elements:
        print("No images found for the given query")
        driver.quit()
        return

    os.makedirs(save_folder, exist_ok=True)

    count = 0
    for img in image_elements:
        if count >= num_images:
            break
        img_url = img.get_attribute('src')
        if img_url:
            try:
                img_path = os.path.join(save_folder, f"image_{count + 1}.jpg")
                urllib.request.urlretrieve(img_url, img_path)
                print(f"Downloaded: {img_path}")
                count += 1
            except Exception as e:
                print(f"Error downloading image: {e}")
    
    print(f"Downloaded {count} images.")
    driver.quit()

# GUI untuk pengaturan
def gui():
    def on_fetch_and_download_click():
        query = entry_query.get()
        num_images = int(entry_num_images.get())
        save_folder = filedialog.askdirectory()
        
        if not query or not save_folder:
            messagebox.showerror("Error", "Search query and save folder must be provided.")
            return
        
        search_pinterest(query, num_images, save_folder)
        messagebox.showinfo("Success", "Images have been downloaded!")

    # Setup GUI
    root = Tk()
    root.title("Pinterest Scraper")

    Label(root, text="Search Query:").pack()
    entry_query = Entry(root)
    entry_query.pack()

    Label(root, text="Number of Images:").pack()
    entry_num_images = Entry(root)
    entry_num_images.pack()

    Button(root, text="Browse", command=lambda: filedialog.askdirectory()).pack()
    Button(root, text="Fetch and Download", command=on_fetch_and_download_click).pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
