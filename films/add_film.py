import os
import sqlite3

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from films.add_film_ui import Ui_Form

class AddFilmWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.save_button.clicked.connect(self.add_film)
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

    def add_film(self):
        watched = 1 if self.ui.is_watched.isChecked() else 0  # если радиобаттон выбран, то 1
        name = self.ui.name_input.text()
        genre = self.ui.genre_input.text()
        year = self.ui.year_input.text()
        notes = self.ui.notes_input.toPlainText()
        image = self.ui.image_input.text()
        if os.path.isfile(image):  # тут то же самое с стандартным изображением
            image = image
        else:
            image = 'films/image.jpg'
        if name and genre and year.isdigit():
            conn = sqlite3.connect('films.sqlite')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO films (name, year, genre, watched, notes, image) VALUES (?, ?, ?, ?, ?, ?)',
                (name, int(year), genre, watched, notes, image))
            reply = QMessageBox.question(self, 'Подтверждение', 'Добавить фильм?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                conn.commit()
                QMessageBox.information(self, "Успех", "Фильм был добавлен")
            else:
                QMessageBox.information(self, 'Выход', 'Фильм не был добавлен')
            conn.close()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Некорректные данные')
