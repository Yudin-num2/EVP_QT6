import sys
import json
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QFileInfo, QDateTime
from PyQt6.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem,
QHeaderView, QDialog, QComboBox, QLabel, QLineEdit, QFileDialog, QDateTimeEdit, QDialogButtonBox,
QScrollArea, QPushButton)
from login_form import Ui_login_form
from main_file import *
from add_task import Ui_Dialog
from operations_table_widget import Ui_operations_table_widget
from complete_task import Ui_elimination_task
from what_to_do import Ui_what_to_do_dialog
from task_info_dialog import Ui_task_info_widget
from database import *
import shutil
import datetime

__version__ = '0.0.2'
path_to_save_image = 'saved_photo_path/'

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_form()       
        self.ui.setupUi(self)
        self.ui.btn_login.clicked.connect(self.check_authorization)
        self.show()
        self.main = None

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
        print(result)
        if result:
            self.main = MainPage(result)
            self.main.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверный логин или пароль")


class MainPage(QMainWindow):
    def __init__(self, user_data):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_data = user_data
        self.username = ' '.join([self.user_data[0][3], self.user_data[0][4]])
        
        self.ui.main_tasks_list.setHorizontalHeaderLabels(["Задача", "Исполнители", "Автор", "Время создания", "Статус"])
        self.ui.main_tasks_list.horizontalHeaderItem(0).setFlags(Qt.ItemFlag.ItemIsSelectable)

        for index in range(0, self.ui.main_tasks_list.columnCount()):
            self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)
        
        self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
        self.update_task_list()
        
        self.ui.main_add_task.clicked.connect(lambda: add_task_dialog.show())
        self.ui.update_tasks_list.clicked.connect(self.update_task_list)
        self.ui.main_tasks_list.itemSelectionChanged.connect(self.open_task)


    def update_task_list(self):
        self.ui.main_tasks_list.setRowCount(0)
        row = 0
        tasks = select_tasks()
        for task in tasks:
            _, task_name, workers_name, status, tech_card, path_to_photo, timestamp, author = task
            self.ui.main_tasks_list.insertRow(row)
            self.ui.main_tasks_list.setItem(row, 0, QTableWidgetItem(task_name))
            self.ui.main_tasks_list.setItem(row, 1, QTableWidgetItem(workers_name))
            self.ui.main_tasks_list.setItem(row, 2, QTableWidgetItem(author))
            self.ui.main_tasks_list.setItem(row, 3, QTableWidgetItem(timestamp.strftime("%d:%m:%Y %H:%M")))
            self.ui.main_tasks_list.setItem(row, 4, QTableWidgetItem(status))
            item = self.ui.main_tasks_list.item(row, 4)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsSelectable)
            if item.text() == 'Создана':
                item.setBackground(QColor(188, 53, 53)) # Тёмно-оранжевый с прозрачностью 0.8
            elif item.text() == 'В работе':
                item.setBackground(QColor(255, 255, 51)) # Желтый с прозрачностью 0.8
            row += 1
    
    def open_task(self):
        selected_indexes = self.ui.main_tasks_list.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            columns_count = self.ui.main_tasks_list.model().columnCount()
            text = []
            for column in range(columns_count):
                index = self.ui.main_tasks_list.model().index(row, column)
                text.append(index.data(Qt.ItemDataRole.DisplayRole))
            print(text)
            if text[-1] == 'Создана':
                if 'ТО' in text[0]:   
                    complete_servicing.show()
                else:
                    self.what_to_do_dialog = WhatToDo(text)
                    self.what_to_do_dialog.show()
            else:
                pass #TODO надо как-то реализовать "Выполнена"
                

class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.workers_combobox = None
        self.ui = Ui_Dialog()
        self.list_of_workers = get_users()
        self.ui.setupUi(self)
        self._workers = [self.ui.worker_combobox]
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
        widget = self._workers[-1]
        widget.deleteLater()
        self.worker_row -= 1
        self._workers.pop()


    def create_task(self):
        if not self.ui.routine_checkbox.isChecked():
            task_text = self.ui.text_task.toPlainText()
            if self._workers:
                workers = [self.ui.worker_combobox.currentText()]
                for combobox in self._workers:
                    workers.append(combobox.currentText())
                workers_string = ', '.join(workers)
            
            if not task_text:
                QMessageBox.warning(self, "Ошибка", "Наименование задачи не может быть пустым")
            
            
            global path_to_save_image
            if self.ui.photo_name:
                photo_path = path_to_save_image + self.ui.photo_name.text()
            else: 
                photo_path = path_to_save_image + '404.jpg'
            print(photo_path)
            add_task(task=task_text, workers=workers_string, photo_name=photo_path)
            MainPage.update_task_list()
        
        else:
            workers_string = ', '.join([self.ui.worker_combobox.currentText()])
            tech_card = self.workers_combobox.currentText()
            machine = self.telerobot_combobox.currentText()
            task = f'{tech_card} | {machine}'
            add_task(task=task, workers=workers_string, tech_card=tech_card)
            MainPage.update_task_list()

    
    def on_checkbox_state_changed(self, state):
        if state == 2:
            self.ui.text_task.setReadOnly(True)
            self.ui.add_photo.setEnabled(False)
            self.ui.add_photo.setToolTip("<html><head/><body><p>При ТО нельзя прикрепить фото</p></body></html>")
            self.ui.text_task.setToolTip(
                "<html><head/><body><p>При ТО нельзя заполнять текст</p><p>Он будет заполнен автоматически</p></body></html>")

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
        global path_to_save_image
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.jpg *.jpeg)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            file_name = QFileInfo(selected_file).fileName()
            self.ui.photo_name.setText(file_name)
            save_path = path_to_save_image + file_name
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
    def __init__(self, task: str = None) -> None:
        super().__init__()

        self.ui = Ui_what_to_do_dialog()
        self.ui.setupUi(self)
        self.task = task
        if self.task[-1] == 'Создана':
            self.get_to_work_button = QPushButton(text='Взять в работу')
            self.ui.gridLayout.addWidget(self.get_to_work_button)
            self.get_to_work_button.clicked.connect(self.get_to_work_handler)
        elif self.task[-1] == 'В работе':
            self.get_to_work_button = QPushButton(text='Закончить работы')
            self.ui.gridLayout.addWidget(self.get_to_work_button)
            self.get_to_work_button.clicked.connect(self.set_complete_status)

        self.ui.task_info_button.clicked.connect(self.task_info_handler)
        self.ui.remove_button.clicked.connect(self.remove_handler)
        self.task = task
        self.task_information = None
        self.data = select_task(task[0])
        

    def get_to_work_handler(self):
        set_new_status(status='В работе', task=self.task[0])
        MainPage.update_task_list()
        self.close()


    def task_info_handler(self):
        self.task_information = TaskInfoDialog(data_task=self.data)
        self.task_information.show()
        self.close()

    def remove_handler(self):
        set_new_status(status='Отменено', task=self.task[0])
        MainPage.update_task_list()
        self.close()

    def set_complete_status(self):
        set_new_status(status='Выполнено', task=self.task[0])
        MainPage.update_task_list()
        self.close()


class TaskInfoDialog(QWidget):
    def __init__(self, data_task) -> None:
        super().__init__()

        self.ui = Ui_task_info_widget()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).clicked.connect(self.update_task)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self.close)
        self.users = get_users()
        _, self.name, self.workers, self.status, self.tech_card, self.path_to_photo, self.timestamp,self.author = data_task
        self.workers = self.workers.split(', ')
        self.ui.name_line_edit.setText(self.name)

        for number, worker in enumerate(self.workers, start=2):
            new_combobox = QComboBox()
            new_combobox.setPlaceholderText(worker)
            new_combobox.addItems(self.users)
            self.ui.gridLayout.addWidget(new_combobox, number, 1)
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        self.worker_label = QLabel('Исполнители')
        self.worker_label.setFont(font)
        self.datetime_label = QLabel('Время создания')
        self.ui.gridLayout.addWidget(self.worker_label, 2, 0, len(self.workers), 1)
        self.datetime_label.setFont(font)
        self.ui.gridLayout.addWidget(self.datetime_label, self.ui.gridLayout.rowCount(), 0)
        self.datetime = QDateTimeEdit()
        self.datetime.setReadOnly(True)
        self.datetime.setDateTime(QDateTime(self.timestamp))
        self.ui.gridLayout.addWidget(self.datetime, self.ui.gridLayout.rowCount() - 1, 1)
        self.image_label = QLabel('Фото')
        self.image_label.setFont(font)
        self.ui.gridLayout.addWidget(self.image_label, self.ui.gridLayout.rowCount(), 0)
        self.scroll_area = QScrollArea()
        self.ui.gridLayout.addWidget(self.scroll_area, self.ui.gridLayout.rowCount() - 1, 1)
        self.image = QLabel()
        self.scroll_area.setWidget(self.image)
        self.scroll_area.setWidgetResizable(True)
        self.image.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        img = QPixmap(self.path_to_photo)
        self.image.setPixmap(img)
        # combobox_index = self.ui.gridLayout.indexOf(self.ui.worker_combobox)
        # self.worker_row, _, _, _ = self.ui.gridLayout.getItemPosition(combobox_index)
        #TODO Добавить + и - иисполнителей (При формировании задачи их может не быть, тут могут назначить)



    def update_task(self):
        pass


    def add_worker(self):
        new_combobox = QComboBox()
        new_combobox.addItems(self.list_of_workers)
        self.worker_row += 1
        self.ui.gridLayout.addWidget(new_combobox, self.worker_row, 0)
        self._workers.append(new_combobox)
        
    
    def remove_worker(self):
        widget = self._workers[-1]
        widget.deleteLater()
        self.worker_row -= 1
        self._workers.pop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    add_task_dialog = AddTaskDialog()
    complete_servicing = CompleteServicing()
    complete_task = CompleteTask()
    sys.exit(app.exec())

