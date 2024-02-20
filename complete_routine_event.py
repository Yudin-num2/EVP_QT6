from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_elimination_of_routine_event(object):
    def setupUi(self, elimination_of_routine_event):
        elimination_of_routine_event.setObjectName("elimination_of_routine_event")
        elimination_of_routine_event.resize(675, 622)
        self.gridLayout = QtWidgets.QGridLayout(elimination_of_routine_event)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=elimination_of_routine_event)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 655, 571))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.task_table = QtWidgets.QTableWidget(parent=self.scrollAreaWidgetContents)
        self.task_table.setColumnCount(2)
        self.task_table.setObjectName("task_table")
        self.task_table.setRowCount(0)
        self.task_table.horizontalHeader().setSortIndicatorShown(False)
        self.task_table.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.task_table, 2, 0, 1, 1)
        self.indicators_table = QtWidgets.QTableWidget(parent=self.scrollAreaWidgetContents)
        self.indicators_table.setColumnCount(2)
        self.indicators_table.setObjectName("indicators_table")
        self.indicators_table.setRowCount(0)
        self.indicators_table.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.indicators_table, 4, 0, 1, 1)
        self.indicators_label = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.indicators_label.setObjectName("indicators_label")
        self.gridLayout_2.addWidget(self.indicators_label, 3, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        self.checkBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.checkBox.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=elimination_of_routine_event)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(elimination_of_routine_event)
        self.buttonBox.accepted.connect(elimination_of_routine_event.accept) # type: ignore
        self.buttonBox.rejected.connect(elimination_of_routine_event.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(elimination_of_routine_event)

    def retranslateUi(self, elimination_of_routine_event):
        _translate = QtCore.QCoreApplication.translate
        elimination_of_routine_event.setWindowTitle(_translate("elimination_of_routine_event", "Регистрация выполнения ТО"))
        self.indicators_label.setText(_translate("elimination_of_routine_event", "Какие показатели были измерены?"))
        self.checkBox.setText(_translate("elimination_of_routine_event", "Отметить всё"))
