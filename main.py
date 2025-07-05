import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool

from tmdb import TMDbClient
from notion_utils import NotionClient
from ui import MovieApp
from worker import MovieFetchWorker

# Load environment variables
load_dotenv()

# Dark Theme
def apply_dark_theme(app):
    dark_stylesheet = """
        QWidget {
            background-color: #1e1e1e;
            color: #dddddd;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
        }
        QLineEdit, QTextEdit {
            background-color: #2b2b2b;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 6px;
        }
        QPushButton {
            background-color: #3a3a3a;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #2d6cdf;
            color: white;
        }
        QLabel {
            color: #dddddd;
        }
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 8px;
        }
        QScrollBar::handle:vertical {
            background: #666;
            border-radius: 4px;
        }
    """
    app.setStyleSheet(dark_stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)

    # Initialize clients
    tmdb_client = TMDbClient(api_key=os.getenv("TMDB_API_KEY"))
    notion_client = NotionClient(
        token=os.getenv("NOTION_API_KEY"),
        database_id=os.getenv("NOTION_DATABASE_ID")
    )

    thread_pool = QThreadPool()
    app_window = MovieApp()

    def handle_movie_search(title):
        app_window.show_spinner()
        worker = MovieFetchWorker(tmdb_client, notion_client, title, app_window)
        worker.signals.log_signal.connect(app_window.append_log)
        worker.signals.finished_signal.connect(app_window.hide_spinner)
        thread_pool.start(worker)

    app_window.movie_searched.connect(handle_movie_search)
    app_window.show()
    sys.exit(app.exec_())
