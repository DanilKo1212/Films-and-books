# Form implementation generated from reading ui file 'books_window.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.table.setObjectName("table")
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table)
        self.add_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.edit_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.edit_button.setObjectName("edit_button")
        self.verticalLayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.info_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.info_button.setObjectName("info_button")
        self.verticalLayout.addWidget(self.info_button)
        self.books_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.books_button.setObjectName("books_button")
        self.verticalLayout.addWidget(self.books_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Книга"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Прочитано"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Заметки"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Изображение"))
        self.add_button.setText(_translate("MainWindow", "Добавить книгу"))
        self.edit_button.setText(_translate("MainWindow", "Редактировать книгу"))
        self.delete_button.setText(_translate("MainWindow", "Удалить книгу"))
        self.info_button.setText(_translate("MainWindow", "Информация о книге"))
        self.books_button.setText(_translate("MainWindow", "Фильмы"))
