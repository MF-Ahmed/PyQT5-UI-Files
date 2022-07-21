import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TabWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tab Widget Application')

        # if the target widget of the layout is provided as an init argument, the
        # layout will be automatically set to it
        vbox = QVBoxLayout(self)

        tabwidget = QTabWidget()
        vbox.addWidget(tabwidget)

        firstTab = FirstTab()
        tabwidget.addTab(firstTab, 'First Tab')
        secondTab = SecondTab()
        tabwidget.addTab(secondTab,'Second Tab')

        firstTab.line.textChanged.connect(secondTab.editor.setPlainText)
        firstTab.btn.clicked.connect(lambda: tabwidget.setCurrentWidget(secondTab))

        self.setLayout(vbox)

class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)
        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)
        self.btn=QPushButton('switch',self)
        self.btn.move(80, 50)
        self.btn.clicked.connect(lambda: SecondTab.display(SecondTab(),self.nameLabel.text()))
class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.editor=QTextEdit()
        self.layout.addWidget(self.editor)
        self.setLayout(self.layout)


    def display(self,text):
        self.editor.setText(text)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    tabwidget = TabWidget()
    tabwidget.resize(500,500)
    tabwidget.show()
    app.exec()