import os
import sqlite3

from PyQt6.QtCore import QSize, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel, QTableWidgetItem

import books.books_window
from films.add_film import AddFilmWindow
from films.edit_film import EditFilmWindow
from films.ui_films import Ui_MainWindow
from films.film_description import FilmInfoWindow


class MainWindow(QMainWindow):
    closed = pyqtSignal()  # сигнал на закрытие чтобы можно было открыть окно авторизации заново
    hidden = pyqtSignal()  # сигнал на скрытие чтобы окно авторизации не появлялось при переключении окон

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add_button.clicked.connect(self.add_film)
        self.ui.edit_button.clicked.connect(self.edit_selected_film)
        self.ui.delete_button.clicked.connect(self.delete_selected_film)
        self.ui.info_button.clicked.connect(self.film_info)
        self.ui.books_button.clicked.connect(self.change_to_books)
        self.load_films()

    def change_to_books(self):
        self.books_window = books.books_window.MainWindow()  # скрывает окно с фильмами и открывает окно с книгами
        self.books_window.show()
        self.hide()
        self.books_window.hidden.connect(lambda: self.show())  # открывает окно заново после скрытия окна с книгами

    def hideEvent(self, a0):
        self.hidden.emit()
        a0.accept()

    def closeEvent(self, a0):
        self.closed.emit()
        a0.accept()

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

    def add_film(self):
        self.add_film_window = AddFilmWindow()
        self.add_film_window.show()
        self.add_film_window.closed.connect(lambda: self.load_films())

    def load_films(self):
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM films')
        films = cursor.fetchall()
        self.ui.table.setRowCount(len(films))
        self.ui.table.setColumnWidth(1, 50)
        for row_index, row_data in enumerate(films):
            self.ui.table.setRowHeight(row_index, 200)
            for column_index, value in enumerate(row_data):
                match (column_index):
                    # тк в таблице отображается не вся инфа с БД, то обрабатываем только определенные столцы
                    case 1:
                        self.ui.table.setItem(row_index, 0, QTableWidgetItem(str(value)))
                    case 4:
                        self.ui.table.setItem(row_index, 1, QTableWidgetItem(str(value)))
                    case 5:
                        self.ui.table.setItem(row_index, 2, QTableWidgetItem(str(value)))
                    case 6:
                        if os.path.isfile(value):  # если есть изображение, то принимем его
                            image = value
                        else:
                            image = 'films/image.jpg'  # если нет, то берём по умолчанию
                        label = QLabel()
                        pixmap = QPixmap(image)
                        label.setPixmap(pixmap.scaled(QSize(300, 200)))
                        self.ui.table.setCellWidget(row_index, 3, label)  # ставит label в ячейку таблицы
        conn.close()

    def edit_selected_film(self):
        selected_row = self.ui.table.currentRow()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            film_id = selected_row + 1
            cursor.execute(f'SELECT * FROM films WHERE id={film_id}')
            data = cursor.fetchone()
            current_data = [  # данные из бд по одному фильму
                data[1],  # name
                data[2],  # year
                data[3],  # genre
                data[4],  # watched
                data[5],  # notes
                data[6]  # image
            ]
            self.edit_film_window = EditFilmWindow(film_id, current_data)
            self.edit_film_window.show()
            self.edit_film_window.closed.connect(lambda: self.load_films())
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите фильм для редактирования')
        cursor.close()
        conn.close()

    def film_info(self):
        selected_row = self.ui.table.currentRow()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            film_id = selected_row + 1
            cursor.execute(f'SELECT * FROM films WHERE id={film_id}')
            data = cursor.fetchone()
            current_data = [
                data[1],  # name
                data[2],  # year
                data[3],  # genre
                data[4],  # watched
                data[5],  # notes
                data[6]  # image
            ]
            self.film_info_window = FilmInfoWindow(current_data)
            self.film_info_window.show()
            self.film_info_window.closed.connect(lambda: self.load_films())
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите фильм для отображения информации')
        cursor.close()
        conn.close()

    def delete_selected_film(self):
        selected_row = self.ui.table.currentRow()
        film_id = selected_row + 1
        if film_id is None:
            QMessageBox.warning(None, "Ошибка", 'Выберите фильм')
            return

        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            try:
                cursor.execute(f"DELETE FROM films WHERE id={film_id}")  # удаление из БД
                reply = QMessageBox.question(self, 'Подтверждение', 'Удалить?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    conn.commit()
                    QMessageBox.information(None, "Успех", "Фильм успешно удалён")

                self.load_films()
            except sqlite3.Error as e:
                QMessageBox.critical(None, "Ошибка", f"Невозможно удалить фильм': {e}")
        else:
            QMessageBox.critical(None, 'Ошибка', 'Не выбран фильм')
        cursor.close()
        conn.close()
