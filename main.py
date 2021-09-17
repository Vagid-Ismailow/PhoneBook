import sys
import datetime
import re
from string import ascii_letters
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi

from repository import phone_book_repository
from main_services import *


def check_valid_email_address(email):
  #  return bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def validate_user_name(nickname):
    #return nickname
    return all(map(lambda c: c in ascii_letters, nickname))


def call_error_message_box(message_text, message_title):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message_text)
    msg.setWindowTitle(message_title)
    msg.exec_()


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("forms/login_window.ui", self)
        self.loginButton.clicked.connect(self.login_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registrationButton.clicked.connect(self.create_registration_window)
        self.restorePasswordButton.clicked.connect(self.create_restore_password_window)
        self.cancelButton.clicked.connect(exit)

        self.user_id = None

        self.userName.setPlaceholderText(" Имя пользователя")
        self.password.setPlaceholderText(" Пароль")

        self.passwordBox.stateChanged.connect(self.show_password)

    def show_password(self):
        if self.password.echoMode() == 2:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)


    def login_function(self):
        user_name = self.userName.text()
        password = self.password.text()
        user = phone_book_repository.login(user_name, password)
        if user != None:
            self.user_id = user[0]
            self.create_user_list_table()
        else:
            call_error_message_box("Введеный пароль или логин неверный", "EROR")

    def create_registration_window(self):
        registration = Registration()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def create_user_list_table(self):
        table_users = TableUsers(self.userName.text(), self.user_id)
        widget.addWidget(table_users)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def create_restore_password_window(self):
        restore_password_window = RestorePasswordWindow()
        widget.addWidget(restore_password_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Registration(QDialog):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("forms/registration_window.ui", self)
        self.sendButton.clicked.connect(self.registration_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cancelButton.clicked.connect(self.cancel_button_function)

        self.userName.setPlaceholderText("Имя пользователя")
        self.password.setPlaceholderText("Пароль")
        self.password2.setPlaceholderText("Повторите пароль")

    def registration_function(self):
        if (self.password.text() == self.password2.text()) and ((self.password.text() or self.password2.text()) != ''):
            password = self.password.text()
            if validate_user_name(self.userName.text()):
                user_name = self.userName.text()
                birth_date = datetime.datetime.strptime(self.birthDate.text(), "%d.%m.%Y")
                user_id = phone_book_repository.addUserIn_users(user_name, password, birth_date)

                table_users = TableUsers(user_name, user_id)
                widget.addWidget(table_users)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            else:
                call_error_message_box("Используйте только аглийский алфавит", "ERROR")
        else:
            call_error_message_box("Пароли должны совпадать", "ERROR")

    def cancel_button_function(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class TableUsers(QDialog):
    def __init__(self, user_name, user_id):
        super(TableUsers, self).__init__()
        loadUi("forms/users_table.ui", self)
        self.tableWidget.setColumnWidth(0, 167)
        self.tableWidget.setColumnWidth(1, 167)
        self.tableWidget.setColumnWidth(2, 150)
        self.user_name = user_name
        self.user_id = user_id

        self.pushButton_1.clicked.connect(lambda: self.filter_users(self.pushButton_1.text()))
        self.pushButton_2.clicked.connect(lambda: self.filter_users(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.filter_users(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.filter_users(self.pushButton_4.text()))
        self.pushButton_5.clicked.connect(lambda: self.filter_users(self.pushButton_5.text()))
        self.pushButton_6.clicked.connect(lambda: self.filter_users(self.pushButton_6.text()))
        self.pushButton_7.clicked.connect(lambda: self.filter_users(self.pushButton_7.text()))
        self.pushButton_8.clicked.connect(lambda: self.filter_users(self.pushButton_8.text()))
        self.pushButton_9.clicked.connect(lambda: self.filter_users(self.pushButton_9.text()))
        self.pushButton_10.clicked.connect(lambda: self.filter_users(self.pushButton_10.text()))
        self.pushButton_11.clicked.connect(lambda: self.filter_users(self.pushButton_11.text()))
        self.pushButton_12.clicked.connect(lambda: self.filter_users(self.pushButton_12.text()))
        self.pushButton_13.clicked.connect(lambda: self.filter_users(self.pushButton_13.text()))
        self.pushButton_14.clicked.connect(self.initTable)

        self.name_label.setText(self.user_name)
        self.initTableWithBirthWeek()

        self.addContactButton.clicked.connect(self.create_add_user_window)
        self.tableWidget.clicked.connect(self.doubleClickedHandle)

    def doubleClickedHandle(self, index):
        user_name = self.tableWidget.item(index.row(), 0).text()
        phone = self.tableWidget.item(index.row(), 1).text()
        birth_date = self.tableWidget.item(index.row(), 2).text()

        self.edit_contact_window = EditContact(self, self.user_id, user_name, phone, birth_date)
        self.edit_contact_window.show()

    def initTableWithBirthWeek(self):
        contacts = phone_book_repository.getUsersByBirthDate(self.user_id)
        row = 0
        self.tableWidget.setRowCount(len(contacts))
        for contact in contacts:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(contact["user_name"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(contact["phone"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(contact["birth_date"])))

            if row % 2 != 0:
                self.tableWidget.item(row, 0).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 1).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 2).setBackground(QtGui.QColor(228, 228, 228))
            row += 1

    def initTable(self):
        contacts = phone_book_repository.getAllUsersByUserId(self.user_id)
        row = 0
        self.tableWidget.setRowCount(len(contacts))
        for contact in contacts:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(contact["user_name"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(contact["phone"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(contact["birth_date"])))

            if row % 2 != 0:
                self.tableWidget.item(row, 0).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 1).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 2).setBackground(QtGui.QColor(228, 228, 228))
            row += 1

    def filter_users(self, button_text):
        button_text_list_character = list(button_text)
        users = phone_book_repository.getAllUsersByUserId(self.user_id)
        filter_users = []

        for user in users:
            if user["user_name"][0] in button_text_list_character:
                filter_users.append(user)

        row = 0
        self.tableWidget.setRowCount(len(filter_users))
        for user in filter_users:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(user["user_name"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(user["phone"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user["birth_date"])))

            if row % 2 != 0:
                self.tableWidget.item(row, 0).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 1).setBackground(QtGui.QColor(228, 228, 228))
                self.tableWidget.item(row, 2).setBackground(QtGui.QColor(228, 228, 228))
            row += 1

    def create_add_user_window(self):
        self.add_contact_window = AddContact(self)
        self.add_contact_window.show()


class RestorePasswordWindow(QDialog):
    def __init__(self):
        super(RestorePasswordWindow, self).__init__()
        loadUi("forms/restore_password_window.ui", self)

        self.emailField.setPlaceholderText("Адрес почты")

        self.cancelButton.clicked.connect(self.cancel_button_function)
        self.sendButton.clicked.connect(self.send_email)

    def send_email(self):
        if check_valid_email_address(self.emailField.text()):
            phone_book_repository.addUserEmailIn_users_email(self.emailField.text())
            self.cancel_button_function()
        else:
            call_error_message_box("Некорректный адрес электронной почты", "Error")

    def cancel_button_function(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AddContact(QDialog):
    def __init__(self, user_table_instance):
        super(AddContact, self).__init__()
        loadUi("forms/add_contact_window.ui", self)
        self.sendButton.clicked.connect(self.add_contact)
        self.cancelButton.clicked.connect(self.cancel_button_function)
        self.user_table_instance = user_table_instance
        self.user_id = self.user_table_instance.user_id
        self.userName.setPlaceholderText("Имя пользователя")
        self.phone.setPlaceholderText("Телефон")
        self.setWindowTitle("Телефонная книга")

    def add_contact(self):
        user_name = self.userName.text()
        phone = self.phone.text()
        birth_date = datetime.datetime.strptime(self.birth_date.text(), "%d.%m.%Y")

        if phone_book_repository.getUserByNamePhoneBirthDate(user_name, phone, birth_date, self.user_id) == None:
            if (user_name and phone and birth_date) != '':
                phone_book_repository.addContactIn_book_users(self.user_id, user_name, phone, birth_date)
                self.user_table_instance.initTable()
                self.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Контакт добавлен: {self.userName.text()}")
                msg.setWindowTitle("Добавление контакта")
                msg.exec_()
            else:
                call_error_message_box("Ошибка в добавлении контакта", "ERROR")
        else:
            call_error_message_box("Контакт уже существует!", "ERROR")

    def cancel_button_function(self):
        self.close()


class EditContact(QDialog):
    def __init__(self, user_table_instance, user_id, name, phone, birth_date):
        super(EditContact, self).__init__()
        loadUi("forms/edit_contact_window.ui", self)

        self.setWindowTitle("Телефонная книга")

        self.user_table_instance = user_table_instance
        self.cancelButton.clicked.connect(self.cancel_button_function)
        self.saveButton.clicked.connect(self.updateContact)
        self.deleteButton.clicked.connect(self.deleteContact)

        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.birth_date = birth_date

        self.initFields()

    def initFields(self):
        self.userNameField.setText(self.name)
        self.phoneField.setText(self.phone)
        self.birthDateField.setDate(datetime.datetime.strptime(self.birth_date, '%Y-%m-%d'))

    def updateContact(self):
        user_name = self.userNameField.text()
        phone = self.phoneField.text()
        birth_date = datetime.datetime.strptime(self.birthDateField.text(), "%d.%m.%Y")

        phone_book_repository.updateUser(self.user_id, self.name, self.phone, self.birth_date, user_name, phone, birth_date)

        self.user_table_instance.initTable()
        self.close()

    def deleteContact(self):
        buttonReply = QMessageBox.question(self, 'Подтвердите действие',
                                           "Вы действительно хотите удалить выбранный контакт?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            phone_book_repository.deleteBookUser(self.user_id, self.name, self.phone, self.birth_date)
            self.user_table_instance.initTable()
            self.close()
        else:
            pass

    def cancel_button_function(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Login()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    # widget.setWindowIcon(QIcon("media/icon.png"))
    widget.setWindowTitle("Телефонная книга")
    widget.show()
    app.exec_()
