from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)


        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        
        button_action = QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        button2_action = QAction("Your button2", self)
        button2_action.setStatusTip("This is your button2")
        button2_action.triggered.connect(self.onMyToolBarButtonClick)
        button2_action.setCheckable(True)
        toolbar.addAction(button2_action)


        
        
        self.setStatusBar(QStatusBar(self))




        
        
    def onMyToolBarButtonClick(self, s):
        print("click", s)    


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
