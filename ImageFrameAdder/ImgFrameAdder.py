import cv2
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# =========================
# GLOBAL STATE
# =========================
images = []
current_index = 0
adjustments = {}

frame_img = None
current_img = None

offset_x = 0
offset_y = 0
zoom = 1.0

drag_x = 0
drag_y = 0

# AI face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# =========================
# LOAD FOLDER
# =========================
def load_folder():
    global images, current_index

    folder = filedialog.askdirectory()
    if not folder:
        return

    images = [
        os.path.join(folder,f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg",".png",".jpeg"))
    ]

    current_index = 0
    load_image()


# =========================
# LOAD FRAME
# =========================
def load_frame():
    global frame_img
    path = filedialog.askopenfilename()
    frame_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    update_preview()


# =========================
# LOAD IMAGE
# =========================
def load_image():
    global current_img, offset_x, offset_y, zoom

    if not images:
        return

    path = images[current_index]
    current_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    adj = adjustments.get(path, {"offset_x":0,"offset_y":0,"zoom":1})
    offset_x = adj["offset_x"]
    offset_y = adj["offset_y"]
    zoom = adj["zoom"]

    update_preview()


# =========================
# AI AUTO CENTER
# =========================
def auto_center():

    global offset_x, offset_y

    gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray,1.2,5)

    if len(faces)==0:
        return

    x,y,w,h = faces[0]

    img_h, img_w = current_img.shape[:2]

    cx = x + w//2
    cy = y + h//2

    offset_x = (img_w//2 - cx) * zoom
    offset_y = (img_h//2 - cy) * zoom

    save_adjustment()
    update_preview()


# =========================
# SAVE PER IMAGE ADJUST
# =========================
def save_adjustment():
    path = images[current_index]
    adjustments[path] = {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "zoom": zoom
    }


# =========================
# PREVIEW (GPU FAST)
# =========================
def update_preview():

    if current_img is None or frame_img is None:
        return

    canvas.delete("all")

    img = cv2.resize(
        current_img,
        None,
        fx=zoom,
        fy=zoom,
        interpolation=cv2.INTER_LINEAR
    )

    fh, fw = frame_img.shape[:2]
    base = np.zeros((fh,fw,4),dtype=np.uint8)

    x = int((fw-img.shape[1])/2 + offset_x)
    y = int((fh-img.shape[0])/2 + offset_y)

    if img.shape[2]==3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    base[y:y+img.shape[0], x:x+img.shape[1]] = img

    overlay = frame_img.copy()
    alpha = overlay[:,:,3]/255.0

    for c in range(3):
        base[:,:,c] = (1-alpha)*base[:,:,c] + alpha*overlay[:,:,c]

    imgtk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(base, cv2.COLOR_BGRA2RGBA)))

    canvas.imgtk = imgtk
    canvas.create_image(0,0,anchor="nw",image=imgtk)


# =========================
# DRAG PAN
# =========================
def start_drag(e):
    global drag_x, drag_y
    drag_x = e.x
    drag_y = e.y

def drag_move(e):
    global offset_x, offset_y, drag_x, drag_y

    offset_x += e.x - drag_x
    offset_y += e.y - drag_y

    drag_x = e.x
    drag_y = e.y

    save_adjustment()
    update_preview()


# =========================
# NAVIGATION
# =========================
def next_img(e=None):
    global current_index
    if current_index < len(images)-1:
        current_index += 1
        load_image()

def prev_img(e=None):
    global current_index
    if current_index > 0:
        current_index -= 1
        load_image()


# =========================
# PRESET SAVE/LOAD
# =========================
def save_preset():
    path = filedialog.asksaveasfilename(defaultextension=".json")
    json.dump(adjustments, open(path,"w"))

def load_preset():
    global adjustments
    path = filedialog.askopenfilename()
    adjustments = json.load(open(path))
    load_image()


# =========================
# UI
# =========================
root = tk.Tk()
root.title("Frame Studio PRO")

top = tk.Frame(root)
top.pack()

tk.Button(top,text="Load Folder",command=load_folder).pack(side="left")
tk.Button(top,text="Load Frame",command=load_frame).pack(side="left")
tk.Button(top,text="AI Auto Center (SPACE)",command=auto_center).pack(side="left")
tk.Button(top,text="Save Preset",command=save_preset).pack(side="left")
tk.Button(top,text="Load Preset",command=load_preset).pack(side="left")

canvas = tk.Canvas(root,width=800,height=600,bg="#222")
canvas.pack()

canvas.bind("<ButtonPress-1>",start_drag)
canvas.bind("<B1-Motion>",drag_move)

root.bind("<Right>",next_img)
root.bind("<Left>",prev_img)
root.bind("<space>",lambda e:auto_center())

root.mainloop()