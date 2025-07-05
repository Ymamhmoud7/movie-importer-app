from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import (
    pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt
)
from PyQt5.QtGui import QFont, QMovie, QColor

class MovieApp(QWidget):
    movie_searched = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Movie Importer")
        self.resize(640, 500)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("🎬 <b>Movie Importer</b>")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #4fc3f7;")
        main_layout.addWidget(title_label)

        # Input
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter movie title...")
        self.input_field.setFixedHeight(38)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #555;
                border-radius: 6px;
                padding: 0 10px;
                font-size: 15px;
                background: #2b2b2b;
                color: #dddddd;
            }
            QLineEdit:focus {
                border: 2px solid #4fc3f7;
            }
        """)
        input_layout.addWidget(self.input_field)

        self.search_button = QPushButton("Fetch & Add")
        self.search_button.setFixedHeight(38)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #dddddd;
                border-radius: 6px;
                padding: 0 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4fc3f7;
                color: #1e1e1e;
            }
        """)

        # Spinner container (for centered scaling)
        self.spinner_container = QWidget()
        self.spinner_container.setFixedSize(38, 38)
        self.spinner_container.setVisible(False)

        self.spinner = QLabel(self.spinner_container)
        self.spinner.setAlignment(Qt.AlignCenter)
        self.spinner.setGeometry(0, 0, 38, 38)
        self.spinner_movie = QMovie("spinner.gif")
        self.spinner.setMovie(self.spinner_movie)

        input_layout.addWidget(self.spinner_container)
        input_layout.addWidget(self.search_button)

        main_layout.addLayout(input_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background: #2b2b2b;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                color: #cccccc;
                line-height: 1.3;
            }
        """)
        main_layout.addWidget(self.log_area)

        footer = QLabel("<small style='color: #777'>YMA ❤️ Movies</small>")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

        self.search_button.clicked.connect(self.on_search)

        self._resize_anim = None

    def on_search(self):
        title = self.input_field.text().strip()
        if not title:
            QMessageBox.warning(self, "Input Error", "Please enter a movie title.")
            return
        self.movie_searched.emit(title)

    def append_log(self, message):
        self.log_area.append(f"<div>{message}</div>")

    def show_spinner(self):
        self.spinner_container.setVisible(True)
        self.spinner_movie.start()

        self._resize_anim = QPropertyAnimation(self.spinner_container, b"geometry")
        geo = self.spinner_container.geometry()
        start_geo = QRect(geo.center().x(), geo.center().y(), 0, 0)
        self._resize_anim.setDuration(300)
        self._resize_anim.setStartValue(start_geo)
        self._resize_anim.setEndValue(geo)
        self._resize_anim.setEasingCurve(QEasingCurve.OutBack)
        self._resize_anim.start()

    def hide_spinner(self):
        self.spinner_container.setVisible(False)
        print("HIDE SPINNER instantly called.")


