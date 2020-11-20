# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Menu(object):
    def setupUiMenu(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowIcon(QtGui.QIcon("icon.png"))
        Dialog.setGeometry(500, 200, 800, 600) 
#########################################################################
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(200, 30, 400, 100))
        self.title.setObjectName("title")
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet(
"QLabel {"
    "border-radius: 20;"
    "color: white;"
    "background-color:rgb(255, 201, 31);"
    "qproperty-alignment: \'AlignVCenter | AlignCenter\';"
"}")  
#########################################################################
        self.pushButton_play = QtWidgets.QPushButton(Dialog)
        self.pushButton_play.setGeometry(QtCore.QRect(300, 200, 200, 75))
        self.pushButton_play.setObjectName("pushButton_play")
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(20)
        self.pushButton_play.setFont(font)
        self.pushButton_play.setStyleSheet(
"QPushButton {"
    "border-radius: 20;"
    "color: white;"
    "background-color:rgb(255, 201, 31);"
"}"
"QPushButton:pressed {"
    "background-color:rgb(246,120,39)"
"}")
#########################################################################
        self.pushButton_options = QtWidgets.QPushButton(Dialog)
        self.pushButton_options.setGeometry(QtCore.QRect(300, 325, 200, 75))
        self.pushButton_options.setObjectName("pushButton_options")
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(20)
        self.pushButton_options.setFont(font)
        self.pushButton_options.setStyleSheet(
"QPushButton {"
    "border-radius: 20;"
    "color: white;"
    "background-color:rgb(255, 201, 31);"
"}"
"QPushButton:pressed {"
    "background-color:rgb(246,120,39)"
"}")
#########################################################################   
        self.pushButton_credits = QtWidgets.QPushButton(Dialog)
        self.pushButton_credits.setGeometry(QtCore.QRect(300, 450, 200, 75))
        self.pushButton_credits.setObjectName("pushButton_credits")
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(20)
        self.pushButton_credits.setFont(font)
        self.pushButton_credits.setStyleSheet(
"QPushButton {"
    "border-radius: 20;"
    "color: white;"
    "background-color:rgb(255, 201, 31);"
"}"
"QPushButton:pressed {"
    "background-color:rgb(246,120,39)"
"}")
#########################################################################
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Super Jeu"))
        self.pushButton_play.setText(_translate("Dialog", "Play"))
        self.pushButton_options.setText(_translate("Dialog", "Options"))
        self.pushButton_credits.setText(_translate("Dialog", "Credits"))
        self.title.setText(_translate("Dialog", "Super Jeu"))
