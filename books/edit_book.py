import os
import sqlite3

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from books.add_book_ui import Ui_Form


class EditBookWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self, book_id, data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.book_id = book_id
        self.data = data
        self.ui.name_input.setText(self.data[0])
        self.ui.year_input.setText(str(self.data[1]))
        self.ui.genre_input.setText(self.data[2])
        self.ui.is_read.setChecked(int(self.data[3]))
        self.ui.notes_input.setPlainText(self.data[4])
        self.ui.image_input.setText(self.data[5])
        self.ui.save_button.clicked.connect(self.edit_book)
        self.ui.image_button.clicked.connect(self.browse_image)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.jpg *.jpeg);;All Files (*)")
        if file_path:
            self.ui.image_input.setText(file_path)

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def edit_book(self):
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
                'UPDATE books SET name = ?, year = ?, genre = ?, read = ?, notes = ?, cover = ? WHERE id = ?',
                (name, int(year), genre, int(read), notes, image, self.book_id))
            reply = QMessageBox.question(self, 'Подтверждение', 'Сохранить изменения?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                conn.commit()
                QMessageBox.information(None, "Успех", "Информация о книге была изменена")
            else:
                QMessageBox.information(self, 'Выход', 'Книга не была изменена')
            conn.close()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Некорректные данные')
