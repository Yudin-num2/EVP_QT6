import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem, QHeaderView, QDialog, QGridLayout, QComboBox
from login_form import Ui_login_form
from main_file import *
from add_task import Ui_Dialog
from database import *


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_form()       
        self.ui.setupUi(self)
        self.ui.password_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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

        # for index in range(0, 2):
        #     self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)

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

            for index in range(0, 3):
                self.ui.main_tasks_list.setItem(row, index, QTableWidgetItem(task[index]))

            item = self.ui.main_tasks_list.item(row, 2)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            row += 1

class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.workers = []
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.list_of_workers = get_users()
        self.ui.worker_combobox.addItems(self.list_of_workers)
        self.ui.add_worker_button.clicked.connect(self.add_worker)
        self.ui.remove_worker_button.clicked.connect(self.remove_worker)
        self.ui.buttonBox.accepted.connect(self.create_task)
    
    def add_worker(self):
        new_combobox = QComboBox()
        new_combobox.addItems(self.list_of_workers)
        row_count = self.ui.gridLayout.rowCount()
        self.ui.gridLayout.addWidget(new_combobox, row_count, 0, 1, 1)
        self.workers.append(new_combobox)

    
    def remove_worker(self):
        if len(self.workers) > 0:
            widget = self.workers[-1]
            widget.deleteLater()
            self.workers.pop()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо наличие хотя бы одного исполнителя")

    def create_task(self):
        task_text = self.ui.text_task.toPlainText()
        workers = [self.ui.worker_combobox.currentText()]
        for combobox in self.workers:
            workers.append(combobox.currentText())
        
        if not task_text:
            QMessageBox.warning(self, "Ошибка", "Наименование задачи не может быть пустым")
        
        workers_string = ' | '.join(workers)
        add_task(task_text, workers_string)
        


            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    main_window = MainPage()
    add_task_dialog = AddTaskDialog()
    sys.exit(app.exec())