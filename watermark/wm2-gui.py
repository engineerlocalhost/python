from PIL import Image, ImageOps
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def add_frame(input_folder, output_folder, frame_image_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        frame_image = Image.open(frame_image_path)
    except IOError:
        messagebox.showerror("Error", f"Unable to open frame image at {frame_image_path}")
        return

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            try:
                image = Image.open(img_path)
            except IOError:
                print(f"Error: Unable to open image {img_path}")
                continue

            # Resize frame to match the size of the image
            frame_resized = frame_image.resize(image.size, Image.LANCZOS)

            # Make sure the frame is in RGBA mode
            if frame_resized.mode != 'RGBA':
                frame_resized = frame_resized.convert('RGBA')

            # Make sure the image is in RGBA mode
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Composite the frame on top of the image
            framed_image = Image.alpha_composite(image, frame_resized)

            # Save the result
            output_path = os.path.join(output_folder, filename)
            framed_image.save(output_path, 'PNG')

            print(f"Frame added to {filename}")

    messagebox.showinfo("Info", "Frames added to all images successfully!")

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)

def select_frame_image():
    file_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    frame_image_entry.delete(0, tk.END)
    frame_image_entry.insert(0, file_selected)

def start_processing():
    input_folder = input_folder_entry.get().strip()
    output_folder = output_folder_entry.get().strip()
    frame_image_path = frame_image_entry.get().strip()

    if not input_folder or not output_folder or not frame_image_path:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    add_frame(input_folder, output_folder, frame_image_path)

# Set up the main window
root = tk.Tk()
root.title("Image Frame Adder")

# Create and place the widgets
tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Frame Image:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
frame_image_entry = tk.Entry(root, width=50)
frame_image_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_frame_image).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Start", command=start_processing).grid(row=3, column=0, columnspan=3, pady=10)

# Run the main loop
root.mainloop()
