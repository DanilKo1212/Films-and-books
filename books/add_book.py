import os
import sqlite3

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from books.add_book_ui import Ui_Form


class AddBookWindow(QWidget):
    closed = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.save_button.clicked.connect(self.add_book)
        self.ui.image_button.clicked.connect(self.browse_image)

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()


    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.jpg *.jpeg);;All Files (*)")
        if file_path:
            self.ui.image_input.setText(file_path)

    def add_book(self):
        read = 1 if self.ui.is_read.isChecked() else 0
        name = self.ui.name_input.text()
        genre = self.ui.genre_input.text()
        year = self.ui.year_input.text()
        notes = self.ui.notes_input.toPlainText()
        image = self.ui.image_input.text()
        if os.path.isfile(image):
            image = image
        else:
            image = 'books/image.jpg'
        if name and genre and year.isdigit():
            conn = sqlite3.connect('films.sqlite')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO books (name, year, genre, read, notes, cover) VALUES (?, ?, ?, ?, ?, ?)',
                (name, int(year), genre, read, notes, image))
            reply = QMessageBox.question(self, 'Подтверждение', 'Добавить книгу?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                conn.commit()
                QMessageBox.information(self, "Успех", "Книга был добавлена")
            else:
                QMessageBox.information(self, 'Выход', 'Книга не была добавлена')
            conn.close()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Некорректные данные')
