# =========================================================
# Install Required Packages:
# WINDOWS & LInux : pip install PyQt6 rawpy
# Tambahaan pada linux : pip install PyQt6 rawpy
# =========================================================



import sys
import os
import shutil
import rawpy

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QVBoxLayout, QWidget,
    QTreeView, QSplitter
)

from PyQt6.QtGui import (
    QPixmap, QImage, QFileSystemModel,
    QShortcut, QKeySequence
)

from PyQt6.QtCore import (
    Qt, QDir, QThread, pyqtSignal, QPoint
)

# ================= CONFIG =================
EXT = (".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng")


# =========================================================
# BACKGROUND IMAGE LOADER
# =========================================================
class ImageLoader(QThread):
    loaded = pyqtSignal(str, QImage)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        try:
            if self.path.lower().endswith(
                (".cr2", ".nef", ".arw", ".dng")
            ):
                with rawpy.imread(self.path) as raw:

                    # FAST embedded thumbnail
                    try:
                        thumb = raw.extract_thumb()
                        if thumb.format == rawpy.ThumbFormat.JPEG:
                            img = QImage.fromData(thumb.data)
                            self.loaded.emit(self.path, img)
                            return
                    except:
                        pass

                    rgb = raw.postprocess(
                        use_camera_wb=True,
                        half_size=True
                    )

                h, w, ch = rgb.shape
                img = QImage(
                    rgb.data, w, h, ch * w,
                    QImage.Format.Format_RGB888
                ).copy()
            else:
                img = QImage(self.path)

            self.loaded.emit(self.path, img)

        except Exception as e:
            print("Load error:", e)


# =========================================================
# MAIN WINDOW
# =========================================================
class PhotoSorter(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SJM Photo Sorter PRO")
        self.resize(1300, 800)

        # ================= STATE =================
        self.source = None
        self.files = []
        self.index = 0
        self.scale = 1.0

        self.image_cache = {}
        self.undo_stack = []

        # drag pan
        self.dragging = False
        self.last_pos = QPoint()
        self.image_pos = QPoint(0, 0)

        # ================= FILE EXPLORER =================
        self.model = QFileSystemModel()
        root = QDir.rootPath()

        self.model.setRootPath(root)
        self.model.setFilter(
            QDir.Filter.AllDirs |
            QDir.Filter.NoDotAndDotDot |
            QDir.Filter.Drives
        )

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(root))
        self.tree.setHeaderHidden(True)

        for i in range(1, 4):
            self.tree.setColumnHidden(i, True)

        self.tree.clicked.connect(self.on_folder_selected)

        # ================= IMAGE PREVIEW =================
        self.label = QLabel("Pilih folder di kiri")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background:#111;color:#ccc;")
        self.label.setMouseTracking(True)

        # ================= WORKFLOW INFO BAR =================
        self.info_bar = QLabel()
        self.info_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_bar.setFixedHeight(42)

        self.info_bar.setStyleSheet("""
            QLabel{
                background:#1b1b1b;
                color:#ddd;
                font-size:13px;
                border-top:1px solid #333;
                padding:6px;
            }
        """)

        # ================= LAYOUT =================
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)
        right_layout.addWidget(self.label, stretch=1)
        right_layout.addWidget(self.info_bar)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 980])

        self.setCentralWidget(splitter)

        # ================= SHORTCUT =================
        QShortcut(Qt.Key.Key_Right, self, activated=self.next_img)
        QShortcut(Qt.Key.Key_Left, self, activated=self.prev_img)
        QShortcut(Qt.Key.Key_Space, self, activated=self.move_ok)
        QShortcut(Qt.Key.Key_Delete, self, activated=self.move_reject)
        QShortcut(QKeySequence.StandardKey.Undo, self, activated=self.undo)

    # =====================================================
    # SELECT FOLDER
    # =====================================================
    def on_folder_selected(self, index):

        path = self.model.filePath(index)
        if not os.path.isdir(path):
            return

        self.source = path

        self.files = sorted([
            f for f in os.listdir(path)
            if f.lower().endswith(EXT)
        ])

        self.index = 0
        self.scale = 1.0
        self.image_cache.clear()
        self.undo_stack.clear()

        self.ok_dir = os.path.join(self.source, "OK")
        self.reject_dir = os.path.join(self.source, "REJECT")

        os.makedirs(self.ok_dir, exist_ok=True)
        os.makedirs(self.reject_dir, exist_ok=True)

        if not self.files:
            self.label.setText("Tidak ada foto")
            return

        self.show_image()

    # =====================================================
    # SHOW IMAGE
    # =====================================================
    def show_image(self):

        if not self.files:
            self.label.clear()
            return

        filename = self.files[self.index]
        path = os.path.join(self.source, filename)

        self.update_workflow_info(False)

        if path in self.image_cache:
            self.render_image(self.image_cache[path])
        else:
            self.loader = ImageLoader(path)
            self.loader.loaded.connect(self.cache_and_show)
            self.loader.start()

        self.preload_next()

    def cache_and_show(self, path, img):
        self.image_cache[path] = img
        self.render_image(img)

    def render_image(self, img):

        pix = QPixmap.fromImage(img)

        pix = pix.scaled(
            self.label.size() * self.scale,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(pix)
        self.update_workflow_info(True)

    # =====================================================
    # PRELOAD NEXT
    # =====================================================
    def preload_next(self):

        if self.index + 1 >= len(self.files):
            return

        filename = self.files[self.index + 1]
        path = os.path.join(self.source, filename)

        if path in self.image_cache:
            return

        self.preloader = ImageLoader(path)
        self.preloader.loaded.connect(
            lambda p, i: self.image_cache.update({p: i})
        )
        self.preloader.start()

    # =====================================================
    # NAVIGATION
    # =====================================================
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

    # =====================================================
    # ZOOM
    # =====================================================
    def wheelEvent(self, event):
        if not self.files:
            return

        delta = event.angleDelta().y() / 120
        self.scale *= (1.15 ** delta)
        self.render_current()

    def render_current(self):
        filename = self.files[self.index]
        path = os.path.join(self.source, filename)
        if path in self.image_cache:
            self.render_image(self.image_cache[path])

    # =====================================================
    # DRAG PAN
    # =====================================================
    def mousePressEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_pos = e.pos()

    def mouseMoveEvent(self, e):
        if self.dragging:
            delta = e.pos() - self.last_pos
            self.label.move(self.label.pos() + delta)
            self.last_pos = e.pos()

    def mouseReleaseEvent(self, e):
        self.dragging = False

    # =====================================================
    # MOVE FILE
    # =====================================================
    def move_ok(self):
        self.move_file(self.ok_dir)

    def move_reject(self):
        self.move_file(self.reject_dir)

    def move_file(self, target):

        if not self.files:
            return

        QApplication.processEvents()
        self.label.clear()

        filename = self.files[self.index]
        src = os.path.join(self.source, filename)
        dst = os.path.join(target, filename)

        shutil.move(src, dst)
        self.undo_stack.append((dst, src, filename))

        del self.files[self.index]

        if self.index >= len(self.files):
            self.index = len(self.files) - 1

        self.show_image()

    # =====================================================
    # UNDO
    # =====================================================
    def undo(self):
        if not self.undo_stack:
            return

        dst, src, filename = self.undo_stack.pop()
        shutil.move(dst, src)
        self.files.insert(self.index, filename)
        self.show_image()

    # =====================================================
    # WORKFLOW INFO BAR
    # =====================================================
    def update_workflow_info(self, cached):

        if not self.files:
            self.info_bar.setText("Pilih folder untuk mulai sorting")
            return

        filename = self.files[self.index]
        total = len(self.files)
        zoom = int(self.scale * 100)

        cache_text = "Cached ✅" if cached else "Loading..."

        text = (
            "SPACE=OK | DEL=REJECT | ← → Navigate | Wheel=Zoom"
            f"    ||    {filename} | {self.index+1}/{total}"
            f" | Zoom {zoom}% | {cache_text}"
        )

        self.info_bar.setText(text)


# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoSorter()
    window.show()
    sys.exit(app.exec())