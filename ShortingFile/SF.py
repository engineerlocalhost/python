import sys, os, shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import rawpy

EXT = (".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng")

class PhotoSorter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SJM Photo Sorter")
        self.resize(1000, 700)

        self.label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        self.files = []
        self.index = 0
        self.scale = 1.0
        self.counter = 1

        self.load_source()

    # =============== LOAD SOURCE =================
    def load_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Pilih Source Folder")
        if not folder:
            sys.exit()

        self.source = folder
        self.ok_folder = os.path.join(folder, "OK")
        os.makedirs(self.ok_folder, exist_ok=True)

        self.files = [
            f for f in os.listdir(folder)
            if f.lower().endswith(EXT)
        ]

        self.show_image()

    # =============== SHOW IMAGE =================
    def show_image(self):
        if not self.files:
            self.label.setText("Tidak ada foto")
            return

        path = os.path.join(self.source, self.files[self.index])

        if path.lower().endswith((".cr2", ".nef", ".arw", ".dng")):
            img = self.load_raw(path)
        else:
            img = QImage(path)

        pix = QPixmap.fromImage(img)
        pix = pix.scaled(
            pix.size() * self.scale,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pix)

    def load_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
        h, w, ch = rgb.shape
        return QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)

    # =============== NAVIGATION =================
    def next_img(self):
        if self.index < len(self.files) - 1:
            self.index += 1
            self.scale = 1.0
            self.show_image()

    def prev_img(self):
        if self.index > 0:
            self.index -= 1
            self.scale = 1.0
            self.show_image()

    # =============== MOVE OK =================
    def move_ok(self):
        filename = self.files[self.index]
        src = os.path.join(self.source, filename)
        ext = os.path.splitext(filename)[1]

        new_name = f"sjm-fileok-{self.counter:03d}{ext}"
        dst = os.path.join(self.ok_folder, new_name)

        shutil.move(src, dst)
        self.counter += 1

        del self.files[self.index]
        if self.index >= len(self.files):
            self.index = len(self.files) - 1

        self.show_image()

    # =============== KEYBOARD =================
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Space:
            self.move_ok()

        elif key == Qt.Key.Key_Right:
            self.next_img()

        elif key == Qt.Key.Key_Left:
            self.prev_img()

        elif key == Qt.Key.Key_Plus:
            self.scale *= 1.2
            self.show_image()

        elif key == Qt.Key.Key_Minus:
            self.scale *= 0.8
            self.show_image()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale *= 1.1
        else:
            self.scale *= 0.9
        self.show_image()

# =============== RUN =================
app = QApplication(sys.argv)
window = PhotoSorter()
window.show()
sys.exit(app.exec())