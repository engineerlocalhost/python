import sys, os, shutil
import rawpy

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget,
    QTreeView, QSplitter
)
from PyQt6.QtGui import (
    QPixmap, QImage, QKeySequence, QFileSystemModel, QShortcut
)
from PyQt6.QtCore import Qt

EXT = (".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng")


class PhotoSorter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SJM Photo Sorter")
        self.resize(1300, 800)

        # ===== STATE =====
        self.source = None
        self.files = []
        self.index = 0
        self.scale = 1.0
        self.counter = 1
        self.undo_stack = []

        # ================= LEFT : FILE EXPLORER =================
        self.model = QFileSystemModel()
        self.model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)

        # FIX: tampilkan nama folder
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setColumnWidth(0, 260)

        self.tree.setRootIndex(
            self.model.index(os.path.expanduser("~"))
        )
        self.tree.clicked.connect(self.on_folder_selected)

        # ================= RIGHT : PREVIEW =================
        self.label = QLabel("Pilih folder di kiri")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background:#111; color:#ccc;")
        self.label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.btn_ok = QPushButton("OK (Space)")
        self.btn_next = QPushButton("Next (→)")

        self.btn_ok.clicked.connect(self.move_ok)
        self.btn_next.clicked.connect(self.next_img)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.label, stretch=1)
        right_layout.addLayout(btn_layout)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # ================= SPLITTER =================
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 980])

        self.setCentralWidget(splitter)
        self.status = self.statusBar()

        # ================= GLOBAL SHORTCUTS =================
        QShortcut(Qt.Key.Key_Space, self, activated=self.move_ok)
        QShortcut(Qt.Key.Key_Right, self, activated=self.next_img)
        QShortcut(Qt.Key.Key_Left, self, activated=self.prev_img)
        QShortcut(QKeySequence.StandardKey.Undo, self, activated=self.undo)
        QShortcut(Qt.Key.Key_Plus, self, activated=self.zoom_in)
        QShortcut(Qt.Key.Key_Equal, self, activated=self.zoom_in)
        QShortcut(Qt.Key.Key_Minus, self, activated=self.zoom_out)

    # ================= FOLDER SELECT =================
    def on_folder_selected(self, index):
        path = self.model.filePath(index)
        if not os.path.isdir(path):
            return

        self.source = path
        self.ok_folder = os.path.join(path, "OK")
        os.makedirs(self.ok_folder, exist_ok=True)

        self.files = [
            f for f in os.listdir(path)
            if f.lower().endswith(EXT)
        ]

        self.index = 0
        self.counter = 1
        self.scale = 1.0
        self.undo_stack.clear()

        if not self.files:
            self.label.setText("Tidak ada foto di folder ini")
            self.label.setPixmap(QPixmap())
            return

        self.label.setFocus()
        self.show_image()

    # ================= SHOW IMAGE =================
    def show_image(self):
        if not self.files or not self.source:
            return

        filename = self.files[self.index]
        path = os.path.join(self.source, filename)

        if path.lower().endswith((".cr2", ".nef", ".arw", ".dng")):
            img = self.load_raw(path)
        else:
            img = QImage(path)

        pix = QPixmap.fromImage(img)
        if pix.isNull():
            return

        pix = pix.scaled(
            self.label.size() * self.scale,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(pix)
        self.update_status()

    def resizeEvent(self, event):
        self.show_image()
        super().resizeEvent(event)

    def load_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
        h, w, ch = rgb.shape
        return QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)

    # ================= STATUS =================
    def update_status(self):
        self.status.showMessage(
            f"{self.index + 1}/{len(self.files)} | OK: {self.counter - 1}"
        )

    # ================= NAVIGATION =================
    def next_img(self):
        if self.files and self.index < len(self.files) - 1:
            self.index += 1
            self.scale = 1.0
            self.show_image()

    def prev_img(self):
        if self.files and self.index > 0:
            self.index -= 1
            self.scale = 1.0
            self.show_image()

    # ================= ZOOM =================
    def zoom_in(self):
        if not self.files:
            return
        self.scale *= 1.2
        self.show_image()

    def zoom_out(self):
        if not self.files:
            return
        self.scale *= 0.8
        self.show_image()

    def wheelEvent(self, event):
        if not self.files:
            return
        self.scale *= 1.1 if event.angleDelta().y() > 0 else 0.9
        self.show_image()

    # ================= MOVE OK =================
    def move_ok(self):
        if not self.files:
            return

        filename = self.files[self.index]
        src = os.path.join(self.source, filename)
        ext = os.path.splitext(filename)[1]

        new_name = f"sjm-fileok-{self.counter:03d}{ext}"
        dst = os.path.join(self.ok_folder, new_name)

        shutil.move(src, dst)
        self.undo_stack.append((dst, src, filename))
        self.counter += 1

        del self.files[self.index]
        if self.index >= len(self.files):
            self.index = len(self.files) - 1

        self.show_image()

    # ================= UNDO =================
    def undo(self):
        if not self.undo_stack:
            return

        dst, src, original = self.undo_stack.pop()
        shutil.move(dst, src)
        self.files.insert(self.index, original)
        self.counter -= 1
        self.show_image()


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoSorter()
    window.show()
    sys.exit(app.exec())
