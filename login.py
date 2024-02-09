import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from login_form import Ui_login_form
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
            QMessageBox.information(self, "Успешная авторизация", "Вы успешно авторизовались")
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверный логин или пароль")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec())