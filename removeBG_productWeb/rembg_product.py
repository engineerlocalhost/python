import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageFilter, ImageTk

# ===============================
# CONFIG
# ===============================
BG_COLOR = (243, 243, 243)
ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".webp")
FINAL_SIZE = (600, 600)
THUMB_SIZE = (300, 300)
OUTPUT_FOLDER_NAME = "shopify_img"
MAX_SOURCE = 5

# ===============================
# IMAGE UTILITIES
# ===============================
def crop_to_object(image, padding):
    bbox = image.getbbox()
    if not bbox:
        return image

    w, h = image.size
    l, t, r, b = bbox
    pad_x = int((r - l) * padding)
    pad_y = int((b - t) * padding)

    return image.crop((
        max(0, l - pad_x),
        max(0, t - pad_y),
        min(w, r + pad_x),
        min(h, b + pad_y)
    ))

def resize_to_square(image, size, bg_color):
    image.thumbnail(size, Image.LANCZOS)
    bg = Image.new("RGB", size, bg_color)
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    bg.paste(image, (x, y))
    return bg

def add_shadow(image):
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    alpha = image.split()[-1]
    shadow.paste((0, 0, 0, 120), mask=alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    return Image.alpha_composite(shadow, image)

# ===============================
# FOLDER UTIL
# ===============================
def get_output_folder(input_folder):
    output = os.path.join(input_folder, OUTPUT_FOLDER_NAME)
    thumb = os.path.join(output, "thumbnail")
    os.makedirs(output, exist_ok=True)
    os.makedirs(thumb, exist_ok=True)
    return output, thumb

# ===============================
# GUI FUNCTIONS
# ===============================
def browse_folder(index):
    folder = filedialog.askdirectory()
    if folder:
        source_entries[index].delete(0, tk.END)
        source_entries[index].insert(0, folder)

def process_all_sources():
    zoom = zoom_slider.get()
    total_success = 0

    for i in range(MAX_SOURCE):
        source = source_entries[i].get().strip()
        code = code_entries[i].get().strip()

        if not source or not code:
            continue  # skip kosong

        output_folder, thumb_folder = get_output_folder(source)
        counter = 1

        for file in os.listdir(source):
            if file.lower().endswith(ALLOWED_EXT):
                try:
                    img = Image.open(os.path.join(source, file)).convert("RGBA")
                    removed = remove(img)
                    cropped = crop_to_object(removed, zoom)

                    bg = Image.new("RGBA", cropped.size, BG_COLOR + (255,))
                    bg.paste(cropped, mask=cropped)

                    final = resize_to_square(
                        add_shadow(bg).convert("RGB"),
                        FINAL_SIZE,
                        BG_COLOR
                    )

                    thumb = resize_to_square(final.copy(), THUMB_SIZE, BG_COLOR)

                    final.save(
                        os.path.join(output_folder, f"{code}_D ({counter}).jpg"),
                        quality=95
                    )
                    thumb.save(
                        os.path.join(thumb_folder, f"{code}_T ({counter}).jpg"),
                        quality=90
                    )

                    counter += 1
                    total_success += 1

                except Exception as e:
                    print("Error:", e)

    messagebox.showinfo(
        "Selesai",
        f"✅ Total {total_success} gambar berhasil diproses"
    )

# ===============================
# GUI LAYOUT
# ===============================
root = tk.Tk()
root.title("Multi Source Photo Product Studio")
root.geometry("760x520")
root.resizable(False, False)

source_entries = []
code_entries = []

for i in range(MAX_SOURCE):
    y = 20 + (i * 80)

    tk.Label(root, text=f"Source Folder {i+1}").place(x=20, y=y)
    src = tk.Entry(root, width=50)
    src.place(x=20, y=y+25)
    source_entries.append(src)

    tk.Button(
        root,
        text="Browse",
        command=lambda idx=i: browse_folder(idx)
    ).place(x=420, y=y+22)

    tk.Label(root, text="Kode Produk").place(x=500, y=y)
    code = tk.Entry(root, width=18)
    code.place(x=500, y=y+25)
    code_entries.append(code)

# Default contoh
code_entries[0].insert(0, "B00833")

tk.Label(root, text="Zoom Level").place(x=20, y=430)
zoom_slider = tk.Scale(
    root, from_=0.03, to=0.15,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=300
)
zoom_slider.set(0.07)
zoom_slider.place(x=20, y=450)

tk.Button(
    root,
    text="🚀 PROSES SEMUA SOURCE",
    command=process_all_sources,
    bg="#4CAF50",
    fg="white",
    width=30,
    height=2
).place(x=380, y=440)

root.mainloop()
