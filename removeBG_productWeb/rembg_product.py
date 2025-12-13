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

# ===============================
# IMAGE UTILITIES
# ===============================
def crop_to_object(image, padding):
    bbox = image.getbbox()
    if not bbox:
        return image

    w, h = image.size
    left, top, right, bottom = bbox

    pad_x = int((right - left) * padding)
    pad_y = int((bottom - top) * padding)

    left = max(0, left - pad_x)
    top = max(0, top - pad_y)
    right = min(w, right + pad_x)
    bottom = min(h, bottom + pad_y)

    return image.crop((left, top, right, bottom))

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
# GUI FUNCTIONS
# ===============================
def select_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder)

def get_output_folder(input_folder):
    output = os.path.join(input_folder, OUTPUT_FOLDER_NAME)
    thumb = os.path.join(output, "thumbnail")
    os.makedirs(output, exist_ok=True)
    os.makedirs(thumb, exist_ok=True)
    return output, thumb

def preview_image():
    folder = input_entry.get()
    if not folder:
        messagebox.showwarning("Warning", "Pilih folder source terlebih dahulu")
        return

    for f in os.listdir(folder):
        if f.lower().endswith(ALLOWED_EXT):
            img = Image.open(os.path.join(folder, f)).convert("RGBA")
            removed = remove(img)
            cropped = crop_to_object(removed, zoom_slider.get())

            bg = Image.new("RGBA", cropped.size, BG_COLOR + (255,))
            bg.paste(cropped, mask=cropped)

            final = resize_to_square(
                add_shadow(bg).convert("RGB"),
                FINAL_SIZE,
                BG_COLOR
            )

            preview = final.resize((260, 260))
            tk_img = ImageTk.PhotoImage(preview)
            preview_label.config(image=tk_img)
            preview_label.image = tk_img
            break

def process_images():
    input_folder = input_entry.get()
    base_code = name_entry.get().strip()

    if not input_folder or not base_code:
        messagebox.showerror(
            "Error",
            "Pilih folder source dan isi Kode Produk (contoh: B00833)"
        )
        return

    output_folder, thumb_folder = get_output_folder(input_folder)
    zoom = zoom_slider.get()
    counter = 1
    success = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(ALLOWED_EXT):
            try:
                img = Image.open(os.path.join(input_folder, filename)).convert("RGBA")
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

                # ===============================
                # FIXED NAMING FORMAT
                # ===============================
                main_name = f"{base_code}_D ({counter})"
                thumb_name = f"{base_code}_T ({counter})"

                final.save(
                    os.path.join(output_folder, f"{main_name}.jpg"),
                    quality=95
                )
                thumb.save(
                    os.path.join(thumb_folder, f"{thumb_name}.jpg"),
                    quality=90
                )

                counter += 1
                success += 1

            except Exception as e:
                print("Error:", e)

    messagebox.showinfo(
        "Selesai",
        f"✅ {success} gambar berhasil diproses\n📁 Output: {output_folder}"
    )

# ===============================
# GUI LAYOUT
# ===============================
root = tk.Tk()
root.title("Photo Product Studio Tool")
root.geometry("720x470")
root.resizable(False, False)

tk.Label(root, text="Folder Source").place(x=20, y=20)
input_entry = tk.Entry(root, width=55)
input_entry.place(x=20, y=45)
tk.Button(root, text="Browse", command=select_input_folder).place(x=470, y=42)

tk.Label(root, text="Kode Produk").place(x=20, y=80)
name_entry = tk.Entry(root, width=30)
name_entry.place(x=20, y=105)
name_entry.insert(0, "B00833")

tk.Label(root, text="Zoom Level").place(x=20, y=145)
zoom_slider = tk.Scale(
    root, from_=0.03, to=0.15,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=300
)
zoom_slider.set(0.07)
zoom_slider.place(x=20, y=165)

tk.Button(root, text="Preview", command=preview_image).place(x=340, y=160)

preview_label = tk.Label(root, bg="#ddd", width=260, height=260)
preview_label.place(x=430, y=145)

tk.Button(
    root,
    text="🚀 PROSES SEMUA GAMBAR",
    command=process_images,
    bg="#4CAF50",
    fg="white",
    width=30,
    height=2
).place(x=200, y=410)

root.mainloop()
