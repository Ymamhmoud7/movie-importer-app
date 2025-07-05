from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

class WorkerSignals(QObject):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

class MovieFetchWorker(QRunnable):
    def __init__(self, tmdb_client, notion_client, title, ui_reference):
        super().__init__()
        self.tmdb_client = tmdb_client
        self.notion_client = notion_client
        self.title = title
        self.ui = ui_reference
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signals.log_signal.emit(f"🔍 Fetching '{self.title}'...")
        metadata = self.tmdb_client.fetch_metadata(self.title)

        if not metadata:
            self.signals.log_signal.emit("❌ Failed to fetch movie metadata.")
            self.signals.finished_signal.emit()
            return

        # Adult content check
        if metadata.get("is_adult"):
            # Must run the dialog in the main thread
            def ask_user():
                reply = QMessageBox.warning(
                    self.ui,
                    "Adult Content",
                    "⚠️ This movie is marked as adult content.\nDo you want to continue adding it?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    self.signals.log_signal.emit(f"❌ Skipped adult movie '{metadata['title']}'")
                    self.signals.finished_signal.emit()
                    return False
                return True

            from PyQt5.QtCore import QMetaObject, Qt, Q_ARG
            accepted = [False]

            def wrapper():
                accepted[0] = ask_user()

            # Execute wrapper synchronously in main thread
            QMetaObject.invokeMethod(
                self.ui,
                wrapper,
                Qt.BlockingQueuedConnection
            )
            if not accepted[0]:
                return

        exists = self.notion_client.check_exists(metadata["title"])
        if exists:
            self.signals.log_signal.emit("⚠️ Movie already exists in Notion.")
            self.signals.finished_signal.emit()
            return

        self.notion_client.create_page(metadata)
        self.signals.log_signal.emit(f"✅ Added '{metadata['title']}' to Notion.")
        self.signals.finished_signal.emit()
