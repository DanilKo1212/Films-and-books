import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox
from ui_auth import Ui_Form
import films.fims_window

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.login)
        self.ui.register_button.clicked.connect(self.register)

    def keyPressEvent(self, event):  # обработка нажатий на кнопки клавиатуры (во всех окнах так)
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):  # на enter вход
            self.login()
        if event.key() == Qt.Key.Key_Escape:  # на esc выход
            self.close()

    def login(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        #  смотрим логин и пароль в бд
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.open_main_window()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

    def register(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        conn = sqlite3.connect('films.sqlite')
        cursor = conn.cursor()
        #  просто вставка новой строки в БД с логин:пароль
        try:
            cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
            conn.commit()
            QMessageBox.information(self, 'Успех', 'Успешно зарегистрирован')
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Ошибка', 'Логин уже зарегистрирован')
        finally:
            conn.close()

    def temp_hide(self):
        self.ui.login_input.clear()
        self.ui.password_input.clear()
        self.hide()

    def open_main_window(self):
        self.main_window = films.fims_window.MainWindow()
        self.main_window.show()
        self.temp_hide()
        self.main_window.closed.connect(lambda: self.show())