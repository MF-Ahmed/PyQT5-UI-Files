# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(556, 414)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button1.setGeometry(QtCore.QRect(200, 230, 171, 101))
        self.Button1.setObjectName("Button1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(190, 50, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.Button1.clicked.connect(lambda: self.messbox("You Just Clicked The Button"))
        #self.actionmenuFile.triggered.connect(lambda: self.messbox("YouJust clicked File"))
        #self.Button1.clicked.connect(self.messbox)

        self.Button1.clicked.connect(self.messbox)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Button1.setText(_translate("MainWindow", "Button1"))
        self.label1.setText(_translate("MainWindow", "Hello My name is Farhan"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

    def messbox(self):
        #self.label1.setText(text)
        #self.label1.adjustSize()
        messB = QMessageBox()
        messB.setWindowTitle("This is a message box")
        messB.setText("You Just Pressesd the Button")
        messB.setIcon(QMessageBox.Information)
        messB.setStandardButtons(QMessageBox.Retry|QMessageBox.Cancel|QMessageBox.Ignore)
        messB.setDetailedText("Information")

        messB.buttonClicked.connect(self.messBPress)        
        i = messB.exec_() 
        #self.show()

    def messBPress(self, j):
        print(j.text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
