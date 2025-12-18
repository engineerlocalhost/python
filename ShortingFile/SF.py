import sys, os, shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QFileDialog,
    QPushButton, QHBoxLayout, QWidget
)
from PyQt6.QtGui import QPixmap, QImage, QKeySequence
from PyQt6.QtCore import Qt
import rawpy

EXT = (".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng")

class PhotoSorter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SJM Photo Sorter")
        self.resize(1100, 750)

        # ===== STATE =====
        self.files = []
        self.index = 0
        self.scale = 1.0
        self.counter = 1
        self.undo_stack = []

        # ===== UI =====
        self.label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_ok = QPushButton("OK (Space)")
        self.btn_next = QPushButton("Next (→)")

        self.btn_ok.clicked.connect(self.move_ok)
        self.btn_next.clicked.connect(self.next_img)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_next)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(main_layout)

        wrapper = QHBoxLayout()
        wrapper.addLayout(main_layout)

        bottom = QHBoxLayout()
        bottom.addLayout(btn_layout)

        layout = QHBoxLayout()
        layout.addWidget(self.label)

        central = QWidget()
        vbox = QHBoxLayout()
        vbox.addWidget(self.label)
        central.setLayout(vbox)

        self.setCentralWidget(central)

        # Button bar
        dock = QWidget(self)
        dock.setLayout(btn_layout)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self._toolbar(dock))

        # Status bar
        self.status = self.statusBar()

        self.load_source()

    def _toolbar(self, widget):
        from PyQt6.QtWidgets import QToolBar
        tb = QToolBar()
        tb.addWidget(widget)
        return tb

    # =============== LOAD SOURCE =================
    def load_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Pilih Source Folder")
        if not folder:
            sys.exit()

        self.source = folder
        self.ok_folder = os.path.join(folder, "OK")
        os.makedirs(self.ok_folder, exist_ok=True)

        self.files = [f for f in os.listdir(folder) if f.lower().endswith(EXT)]
        self.show_image()

    # =============== SHOW IMAGE =================
    def show_image(self):
        if not self.files:
            self.label.setText("Tidak ada foto")
            self.status.showMessage("Selesai")
            return

        filename = self.files[self.index]
        path = os.path.join(self.source, filename)

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

        self.update_status()

    def load_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
        h, w, ch = rgb.shape
        return QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)

    # =============== STATUS BAR =================
    def update_status(self):
        msg = (
            f"File: {self.files[self.index]} | "
            f"Foto: {self.index + 1}/{len(self.files)} | "
            f"OK: {self.counter - 1}"
        )
        self.status.showMessage(msg)

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
        if not self.files:
            return

        filename = self.files[self.index]
        src = os.path.join(self.source, filename)
        ext = os.path.splitext(filename)[1]

        new_name = f"sjm-fileok-{self.counter:03d}{ext}"
        dst = os.path.join(self.ok_folder, new_name)

        shutil.move(src, dst)

        # simpan undo
        self.undo_stack.append((dst, src, filename))
        self.counter += 1

        del self.files[self.index]
        if self.index >= len(self.files):
            self.index = len(self.files) - 1

        self.show_image()

    # =============== UNDO =================
    def undo(self):
        if not self.undo_stack:
            return

        dst, src, original_name = self.undo_stack.pop()
        shutil.move(dst, src)

        self.files.insert(self.index, original_name)
        self.counter -= 1
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

        elif event.matches(QKeySequence.StandardKey.Undo):
            self.undo()

    def wheelEvent(self, event):
        self.scale *= 1.1 if event.angleDelta().y() > 0 else 0.9
        self.show_image()

# =============== RUN =================
app = QApplication(sys.argv)
window = PhotoSorter()
window.show()
sys.exit(app.exec())