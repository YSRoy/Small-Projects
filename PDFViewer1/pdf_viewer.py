#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import fitz  # PyMuPDF
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class PDFViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python PDF Viewer")
        self.resize(900, 700)

        # --- Layout setup ---
        layout = QtWidgets.QVBoxLayout(self)
        topbar = QtWidgets.QHBoxLayout()
        layout.addLayout(topbar)

        # --- Toolbar buttons ---
        self.open_btn = QtWidgets.QPushButton("Open PDF")
        self.prev_btn = QtWidgets.QPushButton("← Prev")
        self.next_btn = QtWidgets.QPushButton("Next →")
        self.zoom_in_btn = QtWidgets.QPushButton("Zoom In")
        self.zoom_out_btn = QtWidgets.QPushButton("Zoom Out")

        for b in [self.open_btn, self.prev_btn, self.next_btn, self.zoom_in_btn, self.zoom_out_btn]:
            topbar.addWidget(b)

        topbar.addStretch()

        self.page_label = QtWidgets.QLabel("Page: 0 / 0")
        topbar.addWidget(self.page_label)

        # --- Scroll area for PDF pages ---
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll.setWidget(self.label)

        # --- Data ---
        self.doc = None
        self.page_count = 0
        self.current_page = 0
        self.zoom = 1.0

        # --- Connect buttons ---
        self.open_btn.clicked.connect(self.open_pdf)
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        # --- Keyboard shortcuts ---
        QtWidgets.QShortcut(QtGui.QKeySequence("Right"), self, activated=self.next_page)
        QtWidgets.QShortcut(QtGui.QKeySequence("Left"), self, activated=self.prev_page)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl++"), self, activated=self.zoom_in)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+-"), self, activated=self.zoom_out)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            self.doc = fitz.open(path)
            self.page_count = self.doc.page_count
            self.current_page = 0
            self.zoom = 1.0
            self.show_page()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF:\n{e}")

    def show_page(self):
        if not self.doc:
            return
        page = self.doc.load_page(self.current_page)
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat)
        img = QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img))
        self.page_label.setText(f"Page: {self.current_page + 1} / {self.page_count}")

    def next_page(self):
        if self.doc and self.current_page < self.page_count - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def zoom_in(self):
        if self.doc:
            self.zoom *= 1.25
            self.show_page()

    def zoom_out(self):
        if self.doc and self.zoom > 0.5:
            self.zoom /= 1.25
            self.show_page()


# --- Universal launcher (works in Jupyter, Spyder, PyInstaller, etc.) ---
def launch_viewer():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    viewer = PDFViewer()
    viewer.show()

    # Jupyter/Spyder environments already have event loops
    # so we avoid exiting the interpreter
    try:
        if hasattr(app, "exec"):
            app.exec()
        else:
            app.exec_()
    except SystemExit:
        pass


if __name__ == "__main__":
    launch_viewer()


# In[ ]:




