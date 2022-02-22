# importing the required libraries

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("round label")

        # setting  the geometry of window
        self.setGeometry(60, 60, 600, 400)

        # creating a label widget
        # by default label will display at top left corner
        self.label_1 = QLabel('round label', self)

        # moving position
        self.label_1.move(100, 100)

        # making label square in size
        self.label_1.resize(80, 80)

        # setting up border and radius
        self.label_1.setStyleSheet("border: 3px solid blue; border-radius: 40px;")

        # show all the widgets
        self.show()

        # create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())

