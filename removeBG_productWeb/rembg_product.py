import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageFilter, ImageTk

# ===============================
# CONFIG
# ===============================
BG_COLOR = (243, 243, 243)   # #f3f3f3
ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".webp")
FINAL_SIZE = (600, 600)
THUMB_SIZE = (300, 300)

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

def visual_centering(image):
    """
    Centering berdasarkan visual weight (bbox tengah)
    """
    bbox = image.getbbox()
    if not bbox:
        return image

    cx = (bbox[0] + bbox[2]) // 2
    cy = (bbox[1] + bbox[3]) // 2
    return image, cx, cy

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
    combined = Image.alpha_composite(shadow, image)
    return combined

# ===============================
# GUI FUNCTIONS
# ===============================
def select_input_folder():
    folder = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder)

def preview_image():
    folder = input_entry.get()
    if not folder:
        return

    for f in os.listdir(folder):
        if f.lower().endswith(ALLOWED_EXT):
            img_path = os.path.join(folder, f)
            img = Image.open(img_path).convert("RGBA")
            removed = remove(img)

            zoom = zoom_slider.get()
            cropped = crop_to_object(removed, zoom)

            bg = Image.new("RGBA", cropped.size, BG_COLOR + (255,))
            bg.paste(cropped, mask=cropped)

            shadowed = add_shadow(bg)
            final = resize_to_square(shadowed.convert("RGB"), FINAL_SIZE, BG_COLOR)

            preview = final.resize((260, 260))
            tk_img = ImageTk.PhotoImage(preview)
            preview_label.config(image=tk_img)
            preview_label.image = tk_img
            break

def process_images():
    input_folder = input_entry.get()
    output_folder = output_entry.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Pilih folder input dan output!")
        return

    zoom = zoom_slider.get()
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, "thumbnail"), exist_ok=True)

    success = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(ALLOWED_EXT):
            try:
                img = Image.open(os.path.join(input_folder, filename)).convert("RGBA")
                removed = remove(img)

                cropped = crop_to_object(removed, zoom)

                bg = Image.new("RGBA", cropped.size, BG_COLOR + (255,))
                bg.paste(cropped, mask=cropped)

                shadowed = add_shadow(bg)

                final = resize_to_square(shadowed.convert("RGB"), FINAL_SIZE, BG_COLOR)
                thumb = resize_to_square(final.copy(), THUMB_SIZE, BG_COLOR)

                name = os.path.splitext(filename)[0]
                final.save(os.path.join(output_folder, f"{name}.jpg"), quality=95)
                thumb.save(os.path.join(output_folder, "thumbnail", f"{name}_thumb.jpg"), quality=90)

                success += 1
            except Exception as e:
                print("Error:", e)

    messagebox.showinfo("Selesai", f"Berhasil memproses {success} gambar")

# ===============================
# GUI LAYOUT
# ===============================
root = tk.Tk()
root.title("Photo Product Studio Tool")
root.geometry("720x420")
root.resizable(False, False)

tk.Label(root, text="Folder Source").place(x=20, y=20)
input_entry = tk.Entry(root, width=50)
input_entry.place(x=20, y=45)
tk.Button(root, text="Browse", command=select_input_folder).place(x=420, y=42)

tk.Label(root, text="Folder Result").place(x=20, y=80)
output_entry = tk.Entry(root, width=50)
output_entry.place(x=20, y=105)
tk.Button(root, text="Browse", command=select_output_folder).place(x=420, y=102)

tk.Label(root, text="Zoom Level").place(x=20, y=150)
zoom_slider = tk.Scale(root, from_=0.03, to=0.15, resolution=0.01, orient=tk.HORIZONTAL, length=300)
zoom_slider.set(0.07)
zoom_slider.place(x=20, y=170)

tk.Button(root, text="Preview", command=preview_image).place(x=340, y=165)

preview_label = tk.Label(root, bg="#ddd", width=260, height=260)
preview_label.place(x=430, y=150)

tk.Button(
    root,
    text="🚀 PROSES SEMUA GAMBAR",
    command=process_images,
    bg="#4CAF50",
    fg="white",
    width=30,
    height=2
).place(x=200, y=360)

root.mainloop()
