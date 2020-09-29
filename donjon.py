import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from ui_menu import Ui_Menu
from ui_donjon import Ui_Calculator



class GameWindow(QtWidgets.QMainWindow, Ui_Menu,Ui_Calculator):
    firNumber = None
    typingNumber = False

    def __init__(self):
        super().__init__()
        self.setupUiMenu(self)
        self.show()
     
        self.pushButton_options.clicked.connect(self.options)

    def options(self):
    	self.setupUiTest(self)
    	print(8)


app = QApplication(sys.argv)
Game = GameWindow()
sys.exit(app.exec())