import sys
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem, QHeaderView, QDialog, QComboBox, QLabel
from login_form import Ui_login_form
from main_file import *
from add_task import Ui_Dialog
from operations_table_widget import Ui_operations_table_widget
from complete_task import Ui_elimination_task
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

        if not login:
            QMessageBox.warning(self, "Ошибка авторизации", "Поле 'логин' не может быть пустым")
            return
        
        elif not passw:
            QMessageBox.warning(self, "Ошибка авторизации", "Поле 'пароль' не может быть пустым")
            return
        
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
        self.ui.main_tasks_list.horizontalHeaderItem(0).setFlags(Qt.ItemFlag.ItemIsSelectable)

        for index in range(0, self.ui.main_tasks_list.columnCount()):
            self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)
        
        self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
        self.update_task_list()
        
        self.ui.main_add_task.clicked.connect(self.show_add_task_dialog)
        self.ui.update_tasks_list.clicked.connect(self.update_task_list)
        self.ui.main_tasks_list.itemSelectionChanged.connect(self.open_task)


    def show_add_task_dialog(self): return add_task_dialog.show()


    def update_task_list(self):
        self.ui.main_tasks_list.setRowCount(0)
        row = 0
        tasks = select_tasks()
        for task in tasks:
            self.ui.main_tasks_list.insertRow(row)
            self.ui.main_tasks_list.setItem(row, 0, QTableWidgetItem(task[0]))
            workers = task[1].replace(' | ', ', ')
            self.ui.main_tasks_list.setItem(row, 1, QTableWidgetItem(workers))
            self.ui.main_tasks_list.setItem(row, 2, QTableWidgetItem(task[2]))
            item = self.ui.main_tasks_list.item(row, 2)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsSelectable)  
            row += 1
    
    def open_task(self):
        selected_items = self.ui.main_tasks_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            if item.column() == 0:
                text = item.text()
                if 'ТО' in text:   
                    complete_servicing.show()
                else:
                    complete_task.ui.name_of_task.setText(text)
                    complete_task.show()



class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.workers_combobox = None
        self._workers = []
        self.ui = Ui_Dialog()
        self.list_of_workers = get_users()
        self.ui.setupUi(self)
        self.ui.worker_combobox.addItems(self.list_of_workers)
        self.ui.add_worker_button.clicked.connect(self.add_worker)
        self.ui.remove_worker_button.clicked.connect(self.remove_worker)
        self.ui.buttonBox.accepted.connect(self.create_task)
        self.ui.checkBox.stateChanged.connect(self.on_checkbox_state_changed)
        #TODO Сделай self.rowcount = и меняй каждый раз, когда добавляешь или удаляешь виджет


    def add_worker(self):
        new_combobox = QComboBox()
        new_combobox.addItems(self.list_of_workers)
        row_count = self.ui.gridLayout.rowCount()
        self.ui.gridLayout.addWidget(new_combobox, row_count, 0)
        self._workers.append(new_combobox)
        
    
    def remove_worker(self):
        if len(self._workers) > 0:
            widget = self._workers[-1]
            widget.deleteLater()
            self._workers.pop()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо наличие хотя бы одного исполнителя")



    def create_task(self):
        if not self.ui.checkBox.isChecked():
            task_text = self.ui.text_task.toPlainText()
            workers = [self.ui.worker_combobox.currentText()]
            for combobox in self._workers:
                workers.append(combobox.currentText())
            
            if not task_text:
                QMessageBox.warning(self, "Ошибка", "Наименование задачи не может быть пустым")
            
            workers_string = ', '.join(workers)
            add_task(task_text, workers_string)
        
        else:
            workers_string = ', '.join([self.ui.worker_combobox.currentText()])
            tech_card = self.workers_combobox.currentText()
            machine = self.telerobot_combobox.currentText()
            task = f'{tech_card} | {machine}'
            add_task(task, workers_string, tech_card)
    
    
    def on_checkbox_state_changed(self, state):
        if state == 2:
            self.ui.text_task.setReadOnly(True)
            if self.workers_combobox is None:
                self.workers_combobox = QComboBox()
                row_position = self.ui.gridLayout.rowCount()
                self.ui.gridLayout.addWidget(self.workers_combobox, row_position, 0)
                technological_cards = select_technological_cards()
                cards = ', '.join([item[0] for item in technological_cards])                    
                self.workers_combobox.addItems(cards.split(', '))

            self.telerobot_label = QLabel()
            self.telerobot_combobox = QComboBox()
            self.telerobot_label.setText('Комплекс')
            self.ui.gridLayout.addWidget(self.telerobot_label, row_position + 1, 0)
            self.ui.gridLayout.addWidget(self.telerobot_combobox, row_position + 2, 0)
            machines_name = select_machines_name()
            names_of_machines = ', '.join([name[0] for name in machines_name])
            self.telerobot_combobox.addItems(names_of_machines.split(', '))

        else:
            self.ui.text_task.setReadOnly(False)
            self.ui.gridLayout.removeWidget(self.telerobot_combobox)
            self.telerobot_combobox.deleteLater()
            self.telerobot_label.deleteLater()
            self.ui.gridLayout.removeWidget(self.telerobot_label)
            if self.workers_combobox is not None:
                self.ui.gridLayout.removeWidget(self.workers_combobox)
                self.workers_combobox.deleteLater()
                self.workers_combobox = None

        
class CompleteTask(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_elimination_task()
        self.ui.setupUi(self)
        self.indicators_comboboxes = []
        self.all_indicators = select_indicators()
        self.ui.plus_indicator_combobox.clicked.connect(self.add_indicator)
        self.ui.minus_indicator_combobox.clicked.connect(self.remove_indicator)
        

    def add_indicator(self):
        new_combobox = QComboBox()
        new_combobox.addItems(self.all_indicators)
        row_count = self.ui.gridLayout.rowCount()
        self.ui.gridLayout.addWidget(new_combobox, row_count, 0)
        self.indicators_comboboxes.append(new_combobox)

    def remove_indicator(self):
        if len(self.indicators_comboboxes) > 0:
            widget = self.indicators_comboboxes[-1]
            widget.deleteLater()
            self.indicators_comboboxes.pop()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо наличие хотя бы одного исполнителя")


class CompleteServicing(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_operations_table_widget()
        self.ui.setupUi(self)

        for index in range(self.ui.operation_table.columnCount()):
            self.ui.operation_table.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    main_window = MainPage()
    add_task_dialog = AddTaskDialog()
    complete_servicing = CompleteServicing()
    complete_task = CompleteTask()
    sys.exit(app.exec())