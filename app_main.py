import sys
import json
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QFileInfo, QDateTime
from PyQt6.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem,
                             QHeaderView, QDialog, QComboBox, QLabel, QLineEdit, QFileDialog, QDateTimeEdit, QDialogButtonBox,
                             QScrollArea, QPushButton, QCompleter, QDoubleSpinBox)
from login_form import Ui_login_form
from main_page import *
from add_task import Ui_Dialog
from operations_table_widget import Ui_operations_table_widget
from what_to_do import Ui_what_to_do_dialog
from task_info_dialog import Ui_task_info_widget
from what_eliminated import Ui_what_eliminated
from sockets_T01 import Ui_SocketsT01
from database import *
import shutil

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
        self.result = None

    def check_authorization(self):
        login = self.ui.login_text.text()
        passw = self.ui.password_text.text()
        if login and passw == 'admin':
            print('Hello, ADMIN')
            self.result = [(1, 'admin', 'admin', 'Ilya', 'Sysoev', '5', None)]
            self.main = MainPage()
            self.main.show()
            self.close()
            return

        if not login:
            QMessageBox.warning(self, "Ошибка авторизации",
                                "Поле 'логин' не может быть пустым")
            return

        elif not passw:
            QMessageBox.warning(self, "Ошибка авторизации",
                                "Поле 'пароль' не может быть пустым")
            return

        self.result = authorization(login=login, passw=passw)
        if self.result:
            print(self.result)
            self.main = MainPage()
            self.main.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка авторизации",
                                "Неверный логин или пароль")


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_data = login_window.result
        self.username = ' '.join([self.user_data[0][3], self.user_data[0][4]])
        self.ui.main_tasks_list.setHorizontalHeaderLabels(
            ["Задача", "Исполнители", "Автор", "Время создания", "Статус"])
        self.ui.main_tasks_list.horizontalHeaderItem(
            0).setFlags(Qt.ItemFlag.ItemIsEnabled)

        for index in range(0, self.ui.main_tasks_list.columnCount()):
            if index != 1:
                self.ui.main_tasks_list.horizontalHeader().setSectionResizeMode(
                    index, QHeaderView.ResizeMode.ResizeToContents)

        self.ui.main_tasks_list.setColumnWidth(1, 200)
        self.ui.main_tasks_list.horizontalHeader().setStretchLastSection(True)
        self.update_task_list()
        self.add_task = AddTaskDialog()
        self.ui.main_add_task.clicked.connect(self.add_task.show)
        self.ui.update_tasks_list.clicked.connect(self.update_task_list)
        self.ui.main_tasks_list.itemSelectionChanged.connect(self.open_task)
        self.ui.update_tasks_list.setToolTip('Обновить таблицу')
        self.ui.actionTelerobot_1.triggered.connect(lambda: self.open_sockets(self.ui.actionTelerobot_1.text()))
        self.sockets01 = None
        self.different_sockets = None
        
        self.ui.statusbar.showMessage(f'Версия приложения: {__version__}')

    def update_task_list(self):
        self.ui.main_tasks_list.setRowCount(0)
        row = 0
        tasks = select_tasks()
        for task in tasks:
            _, task_name, workers_name, status, tech_card, path_to_photo, timestamp, author, *_ = task
            self.ui.main_tasks_list.insertRow(row)

            for col, text in enumerate([task_name, workers_name, author, timestamp.strftime("%d.%m.%Y %H:%M"), status]):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.main_tasks_list.setItem(row, col, item)

                if col == 1:
                    item1 = self.ui.main_tasks_list.item(row, col)
                    item1.setFlags(
                        item1.flags() | Qt.ItemFlag.ItemIsSelectable)
                    item1.setFlags(item1.flags() | Qt.ItemFlag.ItemIsEnabled)
                    item1.setFlags(
                        item1.flags() | Qt.ItemFlag.ItemIsAutoTristate)

                if text == 'Создана':
                    # Тёмно-оранжевый с прозрачностью 0.8
                    item.setBackground(QColor(188, 53, 53))
                elif text == 'В работе':
                    # Золотой с прозрачностью 0.8
                    item.setBackground(QColor(215, 223, 92))
                elif text == 'Отменена':
                    # MediumSlateBlue  #7B68EE
                    item.setBackground(QColor(123, 104, 238))
            row += 1
        self.ui.main_tasks_list.resizeRowsToContents()

    def open_task(self):
        selected_indexes = self.ui.main_tasks_list.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            columns_count = self.ui.main_tasks_list.model().columnCount()
            text = []
            for column in range(columns_count):
                index = self.ui.main_tasks_list.model().index(row, column)
                text.append(index.data(Qt.ItemDataRole.DisplayRole))

            self.what_to_do_dialog = WhatToDo(text, self.size())
            self.what_to_do_dialog.show()
            return self.what_to_do_dialog

    def open_sockets(self, machine):
        print(machine)
        if machine == 'Телеробот 1':
            self.sockets01 = SocketsT01()
            self.sockets01.show()


class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.tech_card_combobox = None
        self.ui = Ui_Dialog()
        self.list_of_workers = get_users()
        self.ui.setupUi(self)
        self._workers = [self.ui.worker_combobox]
        self.ui.worker_combobox.addItems(self.list_of_workers)
        self.ui.add_worker_button.clicked.connect(self.add_worker)
        self.ui.remove_worker_button.clicked.connect(self.remove_worker)
        self.ui.buttonBox.accepted.connect(self.create_task)
        self.ui.routine_checkbox.stateChanged.connect(
            self.on_checkbox_state_changed)
        self.technological_cards = select_technological_cards()
        self.count_row = self.ui.gridLayout.rowCount()
        combobox_index = self.ui.gridLayout.indexOf(self.ui.worker_combobox)
        self.worker_row, _, _, _ = self.ui.gridLayout.getItemPosition(
            combobox_index)
        self.ui.add_photo.clicked.connect(self.attach_photo)
        self.ui.text_task.setToolTip(
            "При ТО нельзя заполнять текст\nОн будет заполнен автоматически")

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
                QMessageBox.warning(
                    self, "Ошибка", "Наименование задачи не может быть пустым")

            global path_to_save_image
            if self.ui.photo_name:
                photo_path = path_to_save_image + self.ui.photo_name.text()
            else:
                photo_path = path_to_save_image + '404.jpg'
            add_task(task=task_text, workers=workers_string,
                     photo_name=photo_path)
        else:
            workers_string = ', '.join([self.ui.worker_combobox.currentText()])
            tech_card = self.tech_card_combobox.currentText()
            machine = self.telerobot_combobox.currentText()
            task = f'{tech_card} | {machine}'
            add_task(task=task, workers=workers_string, tech_card=tech_card)

    def on_checkbox_state_changed(self, state):
        if state == 2:
            self.ui.text_task.setReadOnly(True)
            self.ui.add_photo.setEnabled(False)
            self.ui.add_photo.setToolTip("При ТО нельзя прикрепить фото")

            if self.tech_card_combobox is None:
                checkbox_index = self.ui.gridLayout.indexOf(
                    self.ui.routine_checkbox)
                checkbox_row, checkbox_colomn, _, _ = self.ui.gridLayout.getItemPosition(
                    checkbox_index)
                self.tech_card_combobox = QComboBox()
                self.ui.gridLayout.addWidget(self.tech_card_combobox,
                                             checkbox_row + 1,
                                             checkbox_colomn,
                                             QtCore.Qt.AlignmentFlag.AlignHCenter)
                cards = ' '.join([item[0]
                                 for item in self.technological_cards])
                self.tech_card_combobox.addItems(cards.split(' '))
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
            self.ui.add_photo.setToolTip("Прикрепить фото")
            self.ui.gridLayout.removeWidget(self.telerobot_combobox)
            self.telerobot_combobox.deleteLater()
            if self.tech_card_combobox is not None:
                self.ui.gridLayout.removeWidget(self.tech_card_combobox)
                self.tech_card_combobox.deleteLater()
                self.tech_card_combobox = None

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


class CompleteServicing(QWidget):
    def __init__(self, data_task, parent_size):
        super().__init__()

        self.ui = Ui_operations_table_widget()
        self.ui.setupUi(self)
        self.resize(parent_size)
        self.task_name, self.workers, _, _, _ = data_task
        self.tech_card = self.task_name.split(' ')[0]
        self.tech_operations = select_technological_operations(
            name=self.tech_card)
        self.ui.allin_checkbox.stateChanged.connect(self.on_clicked_all_in)
        self.upload_json = {}
        self.all_buttons = []
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        font.setBold(True)
        self.ui.operation_table.setAlternatingRowColors(True)
        for index in range(self.ui.operation_table.columnCount()):
            self.ui.operation_table.horizontalHeader().setSectionResizeMode(
                index, QHeaderView.ResizeMode.ResizeToContents)

        for key, value in self.tech_operations.items():
            rowPosition = self.ui.operation_table.rowCount()
            self.ui.operation_table.insertRow(rowPosition)
            self.ui.operation_table.setSpan(rowPosition, 0, 1, 2)
            item = QTableWidgetItem(key)
            item.setBackground(QColor('grey'))
            item.setFont(font)
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.ui.operation_table.setItem(rowPosition, 0, item)
            for num, operation in enumerate(value):
                rowPosition += 1
                self.ui.operation_table.insertRow(rowPosition)
                self.ui.operation_table.setItem(
                    rowPosition, 0, QTableWidgetItem(operation))
                self.button = QPushButton()
                self.button.setCheckable(True)
                self.button.setChecked(False)
                self.button.setStyleSheet("background-color: red; margin: 2px")
                self.button.setObjectName(f'button_{num}')
                self.button.clicked.connect(
                    lambda checked, operation=operation: self.on_clicked_button(checked, operation))
                self.upload_json[operation] = 0
                self.all_buttons.append(self.button)
                self.ui.operation_table.setCellWidget(
                    rowPosition, 1, self.button)
        self.all_indicators = select_indicators()
        self.ui.plus_button.clicked.connect(self.add_indicator)
        self.ui.minus_button.clicked.connect(self.remove_indicator)

    def add_indicator(self):
        new_combobox = QComboBox()
        new_combobox.setMaximumWidth(350)
        new_combobox.addItems(self.all_indicators)
        new_combobox.setMaximumHeight(30)
        # TODO Вместо lineedit нужен DoubleEdit (или как-то так), но где-то нужен
        line_edit = QLineEdit()
        # будет ComboBox(для указания "OK\NOK", а не числа). Взять с работы контролируемые показатели
        self.ui.gridLayout.addWidget(
            new_combobox, self.ui.gridLayout.rowCount(), 0)
        self.ui.gridLayout.addWidget(
            line_edit, self.ui.gridLayout.rowCount(), 1, 1, 2)
        self.repair_parts.append([new_combobox, line_edit])

    def remove_indicator(self):
        if len(self.repair_parts) > 0:
            widgets = self.repair_parts[-1]
            for widget in widgets:
                widget.deleteLater()
            self.repair_parts.pop()
        else:
            QMessageBox.warning(
                self, "Ошибка", "Не указано ни одного контролируемого показателя для удаления")

    def on_clicked_button(self, checked, operation):
        button = self.sender()
        if checked:
            button.setStyleSheet("background-color: green; margin: 2px")
            self.upload_json[operation] = 1
        else:
            button.setStyleSheet("background-color: red; margin: 2px")
            self.upload_json[operation] = 0

    def on_clicked_all_in(self, state):
        if state == 2:
            for button in self.all_buttons:
                button.setStyleSheet("background-color: green; margin: 2px")
            self.upload_json = {key: 1 for key in self.upload_json}
        else:
            for button in self.all_buttons:
                button.setStyleSheet("background-color: red; margin: 2px")
            self.upload_json = {key: 0 for key in self.upload_json}


# TODO Добавил массив всех кнопок, далее необходимо реализовать функцию обработки события смены состояния чекбокса "Выполнить всё",
            # функции закрытия окна, добавления в БД (продумать как лучше сделать, чтобы потом было удобно обрабатывать), реализовать
            # возможность добавления контролируемых показателей


class WhatToDo(QDialog):
    def __init__(self, task, parent_size) -> None:
        super().__init__()

        self.ui = Ui_what_to_do_dialog()
        self.ui.setupUi(self)
        self.main_size = parent_size
        self.task = task
        self.ui.back_button.clicked.connect(lambda: self.close())
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        if self.task[-1] == 'Создана':
            self.get_to_work_button = QPushButton(text='Взять в работу')
            self.get_to_work_button.setSizePolicy(size_policy)
            self.get_to_work_button.setFont(font)
            self.ui.gridLayout.addWidget(self.get_to_work_button)
            self.get_to_work_button.clicked.connect(self.get_to_work_handler)
        elif self.task[-1] == 'В работе':
            self.get_to_work_button = QPushButton(text='Закончить работы')
            self.get_to_work_button.setSizePolicy(size_policy)
            self.get_to_work_button.setFont(font)
            self.ui.gridLayout.addWidget(self.get_to_work_button)
            self.get_to_work_button.clicked.connect(self.set_complete_status)
        elif self.task[-1] == 'Отменена':
            self.ui.remove_button.deleteLater()

        self.ui.task_info_button.clicked.connect(self.task_info_handler)
        self.ui.remove_button.clicked.connect(self.remove_handler)
        self.task = task
        self.task_information = None
        self.data = select_task(task[0])

    def get_to_work_handler(self):
        set_new_status(
            status='В работе', task=self.task[0], workers=self.task[1], author=self.task[2])
        self.close()

    def task_info_handler(self):
        self.task_information = TaskInfoDialog(data_task=self.data)
        self.task_information.show()
        self.close()

    def remove_handler(self):
        set_new_status(
            status='Отменена', task=self.task[0], workers=self.task[1], author=self.task[2])
        self.close()

    def set_complete_status(self):
        if 'ТО' in self.data[1].split('-'):
            self.complete_servicing = CompleteServicing(
                self.task, self.main_size)
            self.complete_servicing.show()
        else:
            self.what_eliminated = WhatHasBeenDone(self.task)
            self.what_eliminated.show()
        self.close()


class TaskInfoDialog(QWidget):
    def __init__(self, data_task) -> None:
        super().__init__()

        self.ui = Ui_task_info_widget()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Save).clicked.connect(self.update_task)
        self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).clicked.connect(self.close)
        self.users = get_users()
        self.comboboxes = []
        _, self.name, self.task_workers, self.status, self.tech_card, self.path_to_photo, self.timestamp, self.author, *_ = data_task
        self.task_workers = self.task_workers.split(', ')
        self.ui.name_line_edit.setText(self.name)
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        self.worker_label = QLabel('Исполнители')
        self.worker_label.setFont(font)
        self.datetime_label = QLabel('Время создания')
        self.datetime_label.setFont(font)
        self.ui.gridLayout.addWidget(
            self.datetime_label, self.ui.gridLayout.rowCount(), 0)
        self.datetime = QDateTimeEdit()
        self.datetime.setReadOnly(True)
        self.datetime.setDateTime(QDateTime(self.timestamp))
        self.ui.gridLayout.addWidget(
            self.datetime, self.ui.gridLayout.rowCount() - 1, 1)
        self.image_label = QLabel('Фото')
        self.image_label.setFont(font)
        self.ui.gridLayout.addWidget(
            self.image_label, self.ui.gridLayout.rowCount(), 0)
        self.scroll_area = QScrollArea()
        self.ui.gridLayout.addWidget(
            self.scroll_area, self.ui.gridLayout.rowCount() - 1, 1)
        self.image = QLabel()
        self.scroll_area.setWidget(self.image)
        self.scroll_area.setWidgetResizable(True)
        self.image.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        img = QPixmap(self.path_to_photo)
        scaled_img = img.scaled(500, 500)
        self.image.setPixmap(scaled_img)
        self.ui.gridLayout.addWidget(
            self.worker_label, self.ui.gridLayout.rowCount(), 0)
        self.add_button = QPushButton("+")
        self.add_button.setMaximumWidth(150)
        self.add_button.clicked.connect(self.add_combobox)
        self.ui.gridLayout.addWidget(
            self.add_button, self.ui.gridLayout.rowCount(), 1)
        self.remove_button = QPushButton("-")
        self.remove_button.setMaximumWidth(150)
        self.remove_button.clicked.connect(self.remove_combobox)
        self.ui.gridLayout.addWidget(
            self.remove_button, self.ui.gridLayout.rowCount() - 1, 0)
        for number, worker in enumerate(self.task_workers, start=self.ui.gridLayout.rowCount()):
            new_combobox = QComboBox()
            new_combobox.setEditable(True)
            completer = QCompleter(self.users)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            new_combobox.setCompleter(completer)
            new_combobox.setCurrentText(worker)
            self.ui.gridLayout.addWidget(new_combobox, number, 1)
            self.comboboxes.append(new_combobox)

    def add_combobox(self):
        new_combobox = QComboBox()
        new_combobox.setEditable(True)
        completer = QCompleter(self.users)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        new_combobox.setCompleter(completer)
        new_combobox.setCurrentText("")
        self.ui.gridLayout.addWidget(
            new_combobox, self.ui.gridLayout.rowCount(), 1)
        self.comboboxes.append(new_combobox)

    def remove_combobox(self):
        if len(self.comboboxes) > 0:
            widget = self.comboboxes[-1]
            widget.deleteLater()
            self.comboboxes.pop()
        else:
            QMessageBox.warning(
                self, 'Ошибка', 'Не найдено ни одного исполнителя для удаления')

    def update_task(self):
        task_name = self.ui.name_line_edit.text()
        workers = ', '.join([worker.currentText()
                            for worker in self.comboboxes])
        prev_workers = ', '.join(self.task_workers)
        update_task_info(prev_task_name=self.name,
                         prev_workers=prev_workers, task=task_name, workers=workers)
        self.close()


class WhatHasBeenDone(QWidget):
    def __init__(self, task) -> None:
        super().__init__()
        self.ui = Ui_what_eliminated()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.complete)
        self.ui.buttonBox.rejected.connect(lambda: self.close())
        self.ui.plus_button.clicked.connect(self.add_repair_parts)
        self.ui.minus_button.clicked.connect(self.remove_repair_parts)
        self.repair_parts_boxes = []
        self.repair_parts_list = select_repair_parts()
        self.task = task

    def add_repair_parts(self):
        new_combobox = QComboBox()
        new_combobox.setEditable(True)
        completer = QCompleter([rep_part[0]
                               for rep_part in self.repair_parts_list])
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        new_combobox.setCompleter(completer)
        new_combobox.lineEdit().setPlaceholderText('Выберите запчасть')
        double = QDoubleSpinBox()
        row_count = self.ui.gridLayout.rowCount()
        self.ui.gridLayout.addWidget(new_combobox, row_count, 0)
        self.ui.gridLayout.addWidget(double, row_count, 1)
        self.repair_parts_boxes.append([new_combobox, double])

    def remove_repair_parts(self):
        if len(self.repair_parts_boxes) > 0:
            widgets = self.repair_parts_boxes[-1]
            for widget in widgets:
                widget.deleteLater()
            self.repair_parts_boxes.pop()
        else:
            QMessageBox.warning(
                self, "Ошибка", "Нет ни одной запчасти для удаления")

    def complete(self):
        if len(self.repair_parts_boxes) <= 0:
            set_new_status(
                status='Выполнено', task=self.task[0], workers=self.task[1], author=self.task[2])
        else:
            repair_parts = []
            for rep_part in self.repair_parts_boxes:
                r_part, count = rep_part[0].currentText(), rep_part[1].value()
                repair_parts.append([r_part, count])
        result = '; '.join([f'{item[0]}, {item[1]}' for item in repair_parts])
        set_new_status(
            status='Выполнено', task=self.task[0], workers=self.task[1], author=self.task[2], repair_parts=result)
        self.close()


class SocketsT01(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_SocketsT01()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec())
