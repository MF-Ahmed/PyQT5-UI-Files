from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time





class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.3)
            self.change_value.emit(cnt)


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 ProgressBar"
        self.top = 200
        self.left = 500
        self.width = 300
        self.height = 100
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        self.progressbar = QProgressBar()
        # self.progressbar.setOrientation(Qt.Vertical)
        self.progressbar.setMaximum(100)
        #self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
        #                               "QProgressBar::chunk {background:yellow}")
        # qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white);
        # self.progressbar.setStyleSheet("QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white); }")
        # self.progressbar.setTextVisible(False)
        vbox.addWidget(self.progressbar)
        self.button = QPushButton("Start Progressbar")
        self.button.clicked.connect(self.startProgressBar)
        #self.button.setStyleSheet('background-color:yellow')
        vbox.addWidget(self.button)
        self.setLayout(vbox)
        self.show()

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())