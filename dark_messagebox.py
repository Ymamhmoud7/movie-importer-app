from PyQt5.QtWidgets import QMessageBox

def show_dark_message(parent, title, text, icon=QMessageBox.Information):
    box = QMessageBox(parent)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(icon)
    box.setStyleSheet("""
        QMessageBox {
            background-color: #2b2b2b;
            color: #dddddd;
        }
        QPushButton {
            background-color: #3a3a3a;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px 10px;
            color: #dddddd;
        }
        QPushButton:hover {
            background-color: #505050;
        }
    """)
    box.exec_()
