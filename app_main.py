import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QComboBox
from login_form import Ui_login_form
from main_file import *
from add_task import Ui_Dialog
from database import *


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_form()       
        self.ui.setupUi(self)

        self.ui.btn_login.clicked.connect(self.check_authorization)
        self.show()

    def check_authorization(self):
        login = self.ui.login_text.text()
        passw = self.ui.password_text.text()
        
        result = authorization(login=login, passw=passw)

        if result:
            main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверный логин или пароль")
    
class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.main_tasks_list.setHorizontalHeaderLabels(["Задача", "Исполнители", "Статус"])

        self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.update_task_list()
        self.ui.main_add_task.clicked.connect(self.show_add_task_dialog)
        self.ui.update_tasks_list.clicked.connect(self.update_task_list)

    def show_add_task_dialog(self):
        
        dialog = AddTaskDialog()
        dialog.exec()


    def update_task_list(self):
        self.ui.main_tasks_list.setRowCount(0)
        row = 0
        for task in select_tasks():
            self.ui.main_tasks_list.insertRow(row)
            self.ui.main_tasks_list.setItem(row, 0, QTableWidgetItem(task[0]))
            self.ui.main_tasks_list.setItem(row, 1, QTableWidgetItem(task[1]))
            self.ui.main_tasks_list.setItem(row, 2, QTableWidgetItem(task[2]))
            item = self.ui.main_tasks_list.item(row, 2)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            row += 1

class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.ui.add_worker_button.clicked.connect(self.add_worker)

    def add_worker(self):
        new_combobox = QComboBox()
        self.layout.addWidget(new_combobox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    main_window = MainPage()
    add_task_dialog = AddTaskDialog()
    sys.exit(app.exec())