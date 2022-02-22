import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QMenuBar, QStatusBar
from PyQt5.QtCore import QRect, QMetaObject, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.Qt import Qt


class Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text = 'Hello World'
        self.setGeometry(300, 300, 500, 500)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        print('y')
        self.drawText(event, painter)
        painter.end()

    def drawText(self, event, p):
        p.setPen(QColor(255, 0, 0))
        p.setFont(QFont('Open Sans', 12))
        p.drawText(event.rect(), Qt.AlignCenter, self.text)


def main():
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    app.exec_()


main()