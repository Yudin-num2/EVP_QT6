import sys
from PyQt6.QtWidgets import QApplication, QWidget
from login_form import Ui_login_form


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_form()       
        self.ui.setupUi(self)       
        
        self.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    sys.exit(app.exec())