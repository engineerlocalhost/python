# =========================================================
# INSTALL:
# pip install PyQt6 rawpy
# =========================================================

import sys
import os
import shutil
import rawpy

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTreeView,
    QSplitter,
    QScrollArea
)

from PyQt6.QtGui import (
    QPixmap,
    QImage,
    QFileSystemModel,
    QShortcut
)

from PyQt6.QtCore import (
    Qt,
    QDir,
    QThread,
    pyqtSignal
)

# =========================================================
# CONFIG
# =========================================================
EXT = (
    ".jpg",
    ".jpeg",
    ".png",
    ".cr2",
    ".nef",
    ".arw",
    ".dng"
)


# =========================================================
# IMAGE LOADER THREAD
# =========================================================
class ImageLoader(QThread):

    loaded = pyqtSignal(str, QImage)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):

        try:

            # =================================================
            # RAW FILE
            # =================================================
            if self.path.lower().endswith(
                (".cr2", ".nef", ".arw", ".dng")
            ):

                with rawpy.imread(self.path) as raw:

                    # FAST THUMBNAIL
                    try:

                        thumb = raw.extract_thumb()

                        if thumb.format == rawpy.ThumbFormat.JPEG:

                            img = QImage.fromData(
                                thumb.data
                            )

                            self.loaded.emit(
                                self.path,
                                img
                            )

                            return

                    except:
                        pass

                    rgb = raw.postprocess(
                        use_camera_wb=True,
                        half_size=True
                    )

                h, w, ch = rgb.shape

                img = QImage(
                    rgb.data,
                    w,
                    h,
                    ch * w,
                    QImage.Format.Format_RGB888
                ).copy()

            # =================================================
            # NORMAL IMAGE
            # =================================================
            else:

                img = QImage(self.path)

            self.loaded.emit(
                self.path,
                img
            )

        except Exception as e:

            print("LOAD ERROR:", e)


# =========================================================
# MAIN WINDOW
# =========================================================
class PhotoSorter(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "SJM Photo Sorter PRO"
        )

        self.resize(1500, 900)

        # =================================================
        # STATE
        # =================================================
        self.source = None
        self.files = []
        self.index = 0

        self.scale = 1.0

        self.current_pixmap = None

        self.image_cache = {}

        # =================================================
        # FILE EXPLORER
        # =================================================
        self.model = QFileSystemModel()

        self.model.setFilter(
            QDir.Filter.AllDirs |
            QDir.Filter.NoDotAndDotDot |
            QDir.Filter.Drives
        )

        self.model.setRootPath("")

        self.tree = QTreeView()

        self.tree.setModel(self.model)

        self.tree.setRootIndex(
            self.model.index("")
        )

        self.tree.setHeaderHidden(True)

        for i in range(1, 4):
            self.tree.setColumnHidden(i, True)

        self.tree.setAnimated(True)

        self.tree.setIndentation(18)

        self.tree.clicked.connect(
            self.on_folder_selected
        )

        # =================================================
        # IMAGE LABEL
        # =================================================
        self.label = QLabel()

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.label.setStyleSheet("""
            QLabel{
                background:#111;
                color:#ccc;
            }
        """)

        # =================================================
        # SCROLL AREA
        # =================================================
        self.scroll = QScrollArea()

        self.scroll.setWidget(self.label)

        self.scroll.setWidgetResizable(True)

        self.scroll.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.scroll.setStyleSheet("""
            QScrollArea{
                background:#111;
                border:none;
            }
        """)

        # =================================================
        # INFO BAR
        # =================================================
        self.info_bar = QLabel()

        self.info_bar.setFixedHeight(40)

        self.info_bar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.info_bar.setStyleSheet("""
            QLabel{
                background:#1b1b1b;
                color:#ddd;
                border-top:1px solid #333;
                font-size:13px;
            }
        """)

        # =================================================
        # RIGHT LAYOUT
        # =================================================
        right_layout = QVBoxLayout()

        right_layout.setSpacing(0)

        right_layout.addWidget(
            self.scroll,
            stretch=1
        )

        right_layout.addWidget(
            self.info_bar
        )

        right_widget = QWidget()

        right_widget.setLayout(
            right_layout
        )

        # =================================================
        # SPLITTER
        # =================================================
        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.addWidget(self.tree)

        splitter.addWidget(right_widget)

        splitter.setSizes([320, 1180])

        self.setCentralWidget(splitter)

        # =================================================
        # SHORTCUT
        # =================================================
        QShortcut(
            Qt.Key.Key_Right,
            self,
            activated=self.next_img
        )

        QShortcut(
            Qt.Key.Key_Left,
            self,
            activated=self.prev_img
        )

        QShortcut(
            Qt.Key.Key_Space,
            self,
            activated=self.copy_ok
        )

        # ZOOM SHORTCUT
        QShortcut(
            Qt.Key.Key_Plus,
            self,
            activated=self.zoom_in
        )

        QShortcut(
            Qt.Key.Key_Minus,
            self,
            activated=self.zoom_out
        )

        QShortcut(
            Qt.Key.Key_0,
            self,
            activated=self.reset_zoom
        )

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

        # =================================================
        # OK FOLDER
        # =================================================
        self.ok_dir = os.path.join(
            self.source,
            "OK"
        )

        os.makedirs(
            self.ok_dir,
            exist_ok=True
        )

        if not self.files:

            self.label.setText(
                "Tidak ada foto"
            )

            return

        self.show_image()

    # =====================================================
    # SHOW IMAGE
    # =====================================================
    def show_image(self):

        if not self.files:

            self.label.setText("Selesai ✔")

            self.info_bar.setText(
                "Semua foto selesai dicek"
            )

            return

        # RESET ZOOM
        self.scale = 1.0

        filename = self.files[self.index]

        path = os.path.join(
            self.source,
            filename
        )

        self.update_info(False)

        # =================================================
        # CACHE
        # =================================================
        if path in self.image_cache:

            self.render_image(
                self.image_cache[path]
            )

        else:

            self.loader = ImageLoader(path)

            self.loader.loaded.connect(
                self.cache_and_show
            )

            self.loader.start()

        self.preload_next()

    # =====================================================
    # CACHE & SHOW
    # =====================================================
    def cache_and_show(self, path, img):

        self.image_cache[path] = img

        self.render_image(img)

    # =====================================================
    # RENDER IMAGE
    # =====================================================
    def render_image(self, img):

        self.current_pixmap = QPixmap.fromImage(img)

        self.update_scaled_image()

    # =====================================================
    # UPDATE SCALED IMAGE
    # =====================================================
    def update_scaled_image(self):

        if not self.current_pixmap:
            return

        # =============================================
        # FIT TO SCREEN DULU
        # =============================================
        viewport_size = self.scroll.viewport().size()

        fitted = self.current_pixmap.scaled(
            viewport_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # =============================================
        # APPLY ZOOM
        # =============================================
        final_size = fitted.size() * self.scale

        scaled = self.current_pixmap.scaled(
            final_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(scaled)

        self.label.resize(
            scaled.size()
        )

        self.update_info(True)

    # =====================================================
    # PRELOAD NEXT
    # =====================================================
    def preload_next(self):

        if self.index + 1 >= len(self.files):
            return

        filename = self.files[
            self.index + 1
        ]

        path = os.path.join(
            self.source,
            filename
        )

        if path in self.image_cache:
            return

        self.preloader = ImageLoader(path)

        self.preloader.loaded.connect(
            lambda p, i:
            self.image_cache.update({p: i})
        )

        self.preloader.start()

    # =====================================================
    # NAVIGATION
    # =====================================================
    def next_img(self):

        if self.index < len(self.files) - 1:

            self.index += 1

            self.show_image()

    def prev_img(self):

        if self.index > 0:

            self.index -= 1

            self.show_image()

    # =====================================================
    # COPY TO OK
    # =====================================================
    def copy_ok(self):

        if not self.files:
            return

        filename = self.files[self.index]

        src = os.path.join(
            self.source,
            filename
        )

        dst = os.path.join(
            self.ok_dir,
            filename
        )

        # copy jika belum ada
        if not os.path.exists(dst):

            shutil.copy2(src, dst)

            print("COPIED:", filename)

        # next image
        self.next_img()

    # =====================================================
    # ZOOM
    # =====================================================
    def wheelEvent(self, event):

        if not self.current_pixmap:
            return

        delta = event.angleDelta().y()

        # zoom in
        if delta > 0:

            self.scale *= 1.15

        # zoom out
        else:

            self.scale /= 1.15

        # limit
        self.scale = max(
            0.1,
            min(self.scale, 15)
        )

        self.update_scaled_image()

    def zoom_in(self):

        self.scale *= 1.15

        self.update_scaled_image()

    def zoom_out(self):

        self.scale /= 1.15

        self.update_scaled_image()

    def reset_zoom(self):

        self.scale = 1.0

        self.update_scaled_image()

    # =====================================================
    # RESIZE WINDOW
    # =====================================================
    def resizeEvent(self, event):

        super().resizeEvent(event)

        if self.current_pixmap:

            self.update_scaled_image()

    # =====================================================
    # INFO BAR
    # =====================================================
    def update_info(self, cached):

        if not self.files:

            self.info_bar.setText(
                "Pilih folder"
            )

            return

        filename = self.files[self.index]

        total = len(self.files)

        zoom = int(self.scale * 100)

        cache_text = (
            "Cached ✅"
            if cached else
            "Loading..."
        )

        text = (
            "SPACE=MARK OK | "
            "← → Navigate | "
            "Wheel=Zoom | "
            "+/- Zoom | "
            "0 Reset"
            f"    ||    {filename}"
            f" | {self.index+1}/{total}"
            f" | Zoom {zoom}%"
            f" | {cache_text}"
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