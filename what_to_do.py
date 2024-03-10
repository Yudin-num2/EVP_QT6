# Form implementation generated from reading ui file 'ui_files/what_to_do_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_what_to_do_dialog(object):
    def setupUi(self, what_to_do_dialog):
        what_to_do_dialog.setObjectName("what_to_do_dialog")
        what_to_do_dialog.resize(431, 445)
        icon = QtGui.QIcon.fromTheme("dialog-information")
        what_to_do_dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(what_to_do_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(parent=what_to_do_dialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.remove_button = QtWidgets.QPushButton(parent=what_to_do_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        self.remove_button.setFont(font)
        self.remove_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.remove_button.setObjectName("remove_button")
        self.gridLayout.addWidget(self.remove_button, 4, 0, 1, 1)
        self.get_to_work_button = QtWidgets.QPushButton(parent=what_to_do_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.get_to_work_button.sizePolicy().hasHeightForWidth())
        self.get_to_work_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        self.get_to_work_button.setFont(font)
        self.get_to_work_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.get_to_work_button.setStyleSheet("")
        self.get_to_work_button.setObjectName("get_to_work_button")
        self.gridLayout.addWidget(self.get_to_work_button, 3, 0, 1, 1)
        self.task_info_button = QtWidgets.QPushButton(parent=what_to_do_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task_info_button.sizePolicy().hasHeightForWidth())
        self.task_info_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        self.task_info_button.setFont(font)
        self.task_info_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.task_info_button.setObjectName("task_info_button")
        self.gridLayout.addWidget(self.task_info_button, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.back_button = QtWidgets.QPushButton(parent=what_to_do_dialog)
        self.back_button.setMaximumSize(QtCore.QSize(50, 50))
        self.back_button.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.back_button.setStyleSheet("border-radius: 25%")
        self.back_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui_files/../Images/back_image.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(50, 50))
        self.back_button.setObjectName("back_button")
        self.verticalLayout.addWidget(self.back_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(what_to_do_dialog)
        QtCore.QMetaObject.connectSlotsByName(what_to_do_dialog)

    def retranslateUi(self, what_to_do_dialog):
        _translate = QtCore.QCoreApplication.translate
        what_to_do_dialog.setWindowTitle(_translate("what_to_do_dialog", "Действия с задачей"))
        self.remove_button.setText(_translate("what_to_do_dialog", "Отменить"))
        self.get_to_work_button.setText(_translate("what_to_do_dialog", "Взять в\n"
"работу"))
        self.task_info_button.setText(_translate("what_to_do_dialog", "Показать\n"
"подробности"))
