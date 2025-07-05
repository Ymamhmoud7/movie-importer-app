from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QScrollArea, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"

class MovieSelectionDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Movie")
        self.resize(600, 500)
        self.selected_result = None

        layout = QVBoxLayout(self)
        label = QLabel("Please select the correct movie:")
        layout.addWidget(label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(10)

        for idx, result in enumerate(results[:12]):
            vbox = QVBoxLayout()
            title = result.get("title", "Untitled")
            year = result.get("release_date", "")[:4]
            img_label = QLabel()

            poster_path = result.get("poster_path")
            if poster_path:
                try:
                    url = IMAGE_BASE_URL + poster_path
                    img_data = requests.get(url).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_data)
                    img_label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                except Exception:
                    img_label.setText("(Image error)")
            else:
                img_label.setText("(No image)")

            vbox.addWidget(img_label)
            vbox.addWidget(QLabel(f"{title} ({year})", alignment=Qt.AlignCenter))
            select_btn = QPushButton("Select")
            select_btn.clicked.connect(lambda checked, r=result: self.select_movie(r))
            vbox.addWidget(select_btn)
            grid.addLayout(vbox, idx // 3, idx % 3)

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def select_movie(self, result):
        self.selected_result = result
        self.accept()
