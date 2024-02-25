from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_operations_table_widget(object):
    def setupUi(self, operations_table_widget):
        operations_table_widget.setObjectName("operations_table_widget")
        operations_table_widget.resize(539, 429)
        icon = QtGui.QIcon.fromTheme("applications-engineering")
        operations_table_widget.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(operations_table_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.operation_table = QtWidgets.QTableWidget(parent=operations_table_widget)
        self.operation_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.operation_table.setColumnCount(4)
        self.operation_table.setObjectName("operation_table")
        self.operation_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.operation_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.operation_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.operation_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.operation_table.setHorizontalHeaderItem(3, item)
        self.operation_table.horizontalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.operation_table, 0, 0, 1, 1)
        self.allin_checkbox = QtWidgets.QCheckBox(parent=operations_table_widget)
        self.allin_checkbox.setObjectName("allin_checkbox")
        self.gridLayout.addWidget(self.allin_checkbox, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=operations_table_widget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(operations_table_widget)
        QtCore.QMetaObject.connectSlotsByName(operations_table_widget)

    def retranslateUi(self, operations_table_widget):
        _translate = QtCore.QCoreApplication.translate
        operations_table_widget.setWindowTitle(_translate("operations_table_widget", "Выполнение ТО"))
        item = self.operation_table.horizontalHeaderItem(0)
        item.setText(_translate("operations_table_widget", "Новый столбец"))
        item = self.operation_table.horizontalHeaderItem(1)
        item.setText(_translate("operations_table_widget", "Наименование"))
        item = self.operation_table.horizontalHeaderItem(2)
        item.setText(_translate("operations_table_widget", "Показатель"))
        item = self.operation_table.horizontalHeaderItem(3)
        item.setText(_translate("operations_table_widget", "Выполнено"))
        self.allin_checkbox.setText(_translate("operations_table_widget", "Выполнить всё"))
