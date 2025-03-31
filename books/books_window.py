import os
import sqlite3

from PyQt6.QtCore import QSize, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel, QTableWidgetItem

import films.fims_window
from books.edit_book import EditBookWindow
from books.add_book import AddBookWindow
from books.books_description import BookInfoWindow
from books.books_window_ui import Ui_MainWindow
import films.fims_window


class MainWindow(QMainWindow):
    closed = pyqtSignal()
    hidden = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add_button.clicked.connect(self.add_book)
        self.ui.edit_button.clicked.connect(self.edit_selected_book)
        self.ui.delete_button.clicked.connect(self.delete_selected_book)
        self.ui.info_button.clicked.connect(self.book_info)
        self.ui.books_button.clicked.connect(self.change_to_films)
        self.load_books()

    def change_to_films(self):
        self.films_window = films.fims_window.MainWindow()
        self.films_window.show()
        self.hide()
        self.films_window.hidden.connect(lambda: self.show())

    def hideEvent(self, a0):
        self.hidden.emit()
        a0.accept()

    def closeEvent(self, a0):
        self.closed.emit()
        a0.accept()

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

    def add_book(self):
        self.add_book_window = AddBookWindow()
        self.add_book_window.show()
        self.add_book_window.closed.connect(lambda: self.load_books())

    def load_books(self):
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        self.ui.table.setRowCount(len(books))
        self.ui.table.setColumnWidth(1, 50)
        for row_index, row_data in enumerate(books):
            self.ui.table.setRowHeight(row_index, 200)
            for column_index, value in enumerate(row_data):
                match (column_index):
                    case 1:
                        self.ui.table.setItem(row_index, 0, QTableWidgetItem(str(value)))
                    case 4:
                        self.ui.table.setItem(row_index, 1, QTableWidgetItem(str(value)))
                    case 5:
                        self.ui.table.setItem(row_index, 2, QTableWidgetItem(str(value)))
                    case 6:
                        if os.path.isfile(value):
                            image = value
                        else:
                            image = 'books/image.jpg'
                        label = QLabel()
                        pixmap = QPixmap(image)
                        label.setPixmap(pixmap.scaled(QSize(300, 200)))
                        self.ui.table.setCellWidget(row_index, 3, label)
        conn.close()

    def edit_selected_book(self):
        selected_row = self.ui.table.currentRow()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            book_id = selected_row + 1
            cursor.execute(f'SELECT * FROM books WHERE id={book_id}')
            data = cursor.fetchone()
            current_data = [
                data[1],  # name
                data[2],  # year
                data[3],  # genre
                data[4],  # read
                data[5],  # notes
                data[6]  # image
            ]
            self.edit_film_window = EditBookWindow(book_id, current_data)
            self.edit_film_window.show()
            self.edit_film_window.closed.connect(lambda: self.load_books())
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите книгу для редактирования')
        cursor.close()
        conn.close()

    def book_info(self):
        selected_row = self.ui.table.currentRow()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            book_id = selected_row + 1
            cursor.execute(f'SELECT * FROM books WHERE id={book_id}')
            data = cursor.fetchone()
            current_data = [
                data[1],  # name
                data[2],  # year
                data[3],  # genre
                data[4],  # read
                data[5],  # notes
                data[6]  # image
            ]
            self.book_info_window = BookInfoWindow(current_data)
            self.book_info_window.show()
            self.book_info_window.closed.connect(lambda: self.load_books())
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите книгу для отображения информации')
        cursor.close()
        conn.close()

    def delete_selected_book(self):
        selected_row = self.ui.table.currentRow()
        book_id = selected_row + 1
        if book_id is None:
            QMessageBox.warning(None, "Ошибка", 'Выберите книгу')
            return

        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        if selected_row >= 0:
            try:
                cursor.execute(f"DELETE FROM books WHERE id={book_id}")
                reply = QMessageBox.question(self, 'Подтверждение', 'Удалить?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    conn.commit()
                    QMessageBox.information(None, "Успех", "Книга успешно удалена")

                self.load_books()
            except sqlite3.Error as e:
                QMessageBox.critical(None, "Ошибка", f"Невозможно удалить книгу': {e}")
        else:
            QMessageBox.critical(None, 'Ошибка', 'Не выбрана книга')
        cursor.close()
        conn.close()
