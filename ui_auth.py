# Form implementation generated from reading ui file 'ui_auth.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(170, 146)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.login_input = QtWidgets.QLineEdit(parent=Form)
        self.login_input.setObjectName("login_input")
        self.verticalLayout.addWidget(self.login_input)
        self.password_input = QtWidgets.QLineEdit(parent=Form)
        self.password_input.setObjectName("password_input")
        self.verticalLayout.addWidget(self.password_input)
        self.login_button = QtWidgets.QPushButton(parent=Form)
        self.login_button.setObjectName("login_button")
        self.verticalLayout.addWidget(self.login_button)
        self.register_button = QtWidgets.QPushButton(parent=Form)
        self.register_button.setObjectName("register_button")
        self.verticalLayout.addWidget(self.register_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login_input.setPlaceholderText(_translate("Form", "Логин"))
        self.password_input.setPlaceholderText(_translate("Form", "Пароль"))
        self.login_button.setText(_translate("Form", "Войти"))
        self.register_button.setText(_translate("Form", "Регистрация"))
