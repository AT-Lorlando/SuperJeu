import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ui_menu import Ui_Menu



class GameWindow(QtWidgets.QMainWindow, Ui_Menu):
    firNumber = None
    typingNumber = False

    def __init__(self):
        super().__init__()
        self.setupUiMenu(self)
        self.show()
     
        self.pushButton_options.clicked.connect(self.options)

    def options(self):
    	print(2)


app = QApplication(sys.argv)
Game = GameWindow()
sys.exit(app.exec())