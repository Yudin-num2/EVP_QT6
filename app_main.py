import sys
import json
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem,
QHeaderView, QDialog, QComboBox, QLabel, QLineEdit, QFileDialog)
from login_form import Ui_login_form
from main_file import *
from add_task import Ui_Dialog
from operations_table_widget import Ui_operations_table_widget
from complete_task import Ui_elimination_task
from what_to_do import Ui_what_to_do_dialog
from database import *
import shutil


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
            if item.text() == 'Создана':
                item.setBackground(QColor(188, 53, 53)) # Тёмно-оранжевый с прозрачностью 0.8
            row += 1
    
    def open_task(self):
        selected_items = self.ui.main_tasks_list.selectedItems()
        print(selected_items[0].text())
        if selected_items:
            item = selected_items[0]
            text = item.text()
            if 'ТО' in text:   
                complete_servicing.show()
            else:
                complete_task.ui.name_of_task.setText(text)
                what_to_do.show()
                

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
        self.ui.routine_checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        self.technological_cards = select_technological_cards()
        self.count_row = self.ui.gridLayout.rowCount()
        combobox_index = self.ui.gridLayout.indexOf(self.ui.worker_combobox)
        self.worker_row, _, _, _ = self.ui.gridLayout.getItemPosition(combobox_index)
        self.ui.add_photo.clicked.connect(self.attach_photo)


    def add_worker(self):
        
        new_combobox = QComboBox()
        new_combobox.addItems(self.list_of_workers)
        self.worker_row += 1
        self.ui.gridLayout.addWidget(new_combobox, self.worker_row, 0)
        self._workers.append(new_combobox)
        
    
    def remove_worker(self):
        if len(self._workers) > 0:
            widget = self._workers[-1]
            widget.deleteLater()
            self.worker_row -= 1
            self._workers.pop()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо наличие хотя бы одного исполнителя")


    def create_task(self):
        if not self.ui.routine_checkbox.isChecked():
            task_text = self.ui.text_task.toPlainText()
            workers = [self.ui.worker_combobox.currentText()]
            for combobox in self._workers:
                workers.append(combobox.currentText())
            
            if not task_text:
                QMessageBox.warning(self, "Ошибка", "Наименование задачи не может быть пустым")
            
            workers_string = ', '.join(workers)
            if self.ui.photo_name:
                photo_path = f"saved_photo_path/{self.ui.photo_name.text()}"
            add_task(task_text, workers_string, photo_path)
        
        else:
            workers_string = ', '.join([self.ui.worker_combobox.currentText()])
            tech_card = self.workers_combobox.currentText()
            machine = self.telerobot_combobox.currentText()
            task = f'{tech_card} | {machine}'
            add_task(task, workers_string, tech_card)
    
    
    def on_checkbox_state_changed(self, state):
        if state == 2:
            self.ui.text_task.setReadOnly(True)
            self.ui.add_photo.setEnabled(False)
            self.ui.add_photo.setToolTip("<html><head/><body><p>При ТО нельзя прикрепить фото</p></body></html>")
            if self.workers_combobox is None:
                checkbox_index = self.ui.gridLayout.indexOf(self.ui.routine_checkbox)
                checkbox_row, checkbox_colomn, _, _ = self.ui.gridLayout.getItemPosition(checkbox_index)
                self.workers_combobox = QComboBox()
                self.ui.gridLayout.addWidget(self.workers_combobox,
                                             checkbox_row + 1,
                                             checkbox_colomn,
                                             QtCore.Qt.AlignmentFlag.AlignHCenter)
                cards = ' '.join([item[0] for item in self.technological_cards])                    
                self.workers_combobox.addItems(cards.split(' '))
            self.telerobot_combobox = QComboBox()
            self.ui.gridLayout.addWidget(self.telerobot_combobox,
                                         checkbox_row + 2,
                                         checkbox_colomn,
                                         QtCore.Qt.AlignmentFlag.AlignHCenter)
            machines_name = select_machines_name()
            names_of_machines = ', '.join([name[0] for name in machines_name])
            self.telerobot_combobox.addItems(names_of_machines.split(', '))
        else:
            self.ui.text_task.setReadOnly(False)
            self.ui.add_photo.setEnabled(True)
            self.ui.add_photo.setToolTip("<html><head/><body><p>Прикрепить фото</p></body></html>")
            self.ui.gridLayout.removeWidget(self.telerobot_combobox)
            self.telerobot_combobox.deleteLater()
            if self.workers_combobox is not None:
                self.ui.gridLayout.removeWidget(self.workers_combobox)
                self.workers_combobox.deleteLater()
                self.workers_combobox = None

    def attach_photo(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.jpg *.jpeg)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            file_name = QFileInfo(selected_file).fileName()
            self.ui.photo_name.setText(file_name)
            save_path = "saved_photo_path/" + file_name
            shutil.copy(selected_file, save_path)
        
class CompleteTask(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_elimination_task()
        self.ui.setupUi(self)
        self.indicators = []
        self.all_indicators = select_indicators()
        self.ui.plus_indicator_combobox.clicked.connect(self.add_indicator)
        self.ui.minus_indicator_combobox.clicked.connect(self.remove_indicator)
        

    def add_indicator(self):
        new_combobox = QComboBox()
        new_combobox.setMaximumWidth(350)
        new_combobox.addItems(self.all_indicators)
        new_combobox.setMaximumHeight(30)
        line_edit = QLineEdit()
        row_count = self.ui.gridLayout.rowCount()
        self.ui.gridLayout.addWidget(new_combobox, row_count, 0)
        self.ui.gridLayout.addWidget(line_edit, row_count, 1, 1, 2)
        self.indicators.append([new_combobox, line_edit])

    def remove_indicator(self):
        if len(self.indicators) > 0:
            widgets = self.indicators[-1]
            for widget in widgets:
                widget.deleteLater()
            self.indicators.pop()
        else:
            QMessageBox.warning(self, "Ошибка", "Не указано ни одного контролируемого показателя для удаления")


class CompleteServicing(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_operations_table_widget()
        self.ui.setupUi(self)

        for index in range(self.ui.operation_table.columnCount()):
            self.ui.operation_table.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)


class WhatToDo(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_what_to_do_dialog()
        self.ui.setupUi(self)
        
        self.ui.task_info_button.clicked.connect(self.task_info_handler)
        self.ui.get_to_work_button.clicked.connect(self.get_to_work_handler)
        self.ui.remove_button.clicked.connect(self.remove_handler)
        

    def get_to_work_handler(self):
        pass


    def task_info_handler(self):
        pass

    def remove_handler(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    main_window = MainPage()
    add_task_dialog = AddTaskDialog()
    complete_servicing = CompleteServicing()
    complete_task = CompleteTask()
    what_to_do = WhatToDo()
    sys.exit(app.exec())

