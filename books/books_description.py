import sqlite3

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from books.info_ui import Ui_Form

class BookInfoWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.name_label.setText(data[0])
        self.ui.year_label.setText(str(data[1]))
        self.ui.genre_label.setText(data[2])
        self.ui.read_label.setText('Прочитанно' if data[3] == 1 else "Не прочитанно")
        self.ui.notes_label.setText(data[4])
        image = data[5]
        pixmap = QPixmap(image)
        self.ui.image_label.setPixmap(pixmap.scaled(QSize(500,500)))
        self.ui.image_label.show()

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
