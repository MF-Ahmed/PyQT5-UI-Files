# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 20:49:32 2019
@author: Tiny
"""
# =============================================================================
''' Mouse event, each action response event can be customized '''

''' Reference: 1. https://blog.csdn.net/richenyunqi/article/details/80554257
                          Pyqt determines the mouse click event - left button press, middle button press, right button press, left and right button press, etc.;
         2. https://fennbk.com/8065
                          Pyqt5 mouse (introduction to events and methods)
         3. https://blog.csdn.net/leemboy/article/details/80462632
                          PyQt5 Programming - Mouse Events
         4. https://doc.qt.io/qtforpython/PySide2/QtGui/QWheelEvent.html#PySide2.QtGui.PySide2.QtGui.QWheelEvent.delta
            QWheelEvent'''
# =============================================================================
# =============================================================================
''' PyQt4 and PyQt5 difference: '''
#   PySide2.QtGui.QWheelEvent.delta()
#   Return type:	int
#   This function has been deprecated, use pixelDelta() or angleDelta() instead.
# =============================================================================
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

'''Custom QLabel class'''


class myImgLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(myImgLabel, self).__init__(parent)
        f = QFont("ZYSong18030", 10)  # Set the font, font size
        self.setFont(f)  # After the event is not defined, the two sentences are deleted or commented out.

    '''Reload the mouse click event (click) '''


def mousePressEvent(self, event):
    If
    event.buttons() == QtCore.Qt.LeftButton:  # left button pressed
    self.setText("Click the left mouse button for the event: define it yourself")
    Print("Click the left mouse button")  # response test statement


Elif
event.buttons() == QtCore.Qt.RightButton:  # right click
self.setText("Click the right mouse button for the event: define it yourself")
Print("right click")  # response test statement
Elif
event.buttons() == QtCore.Qt.MidButton:  # Press
self.setText("Click the middle mouse button for the event: define it yourself")
Print("click the middle mouse button")  # response test statement
Elif
event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # Left and right buttons simultaneously pressed
self.setText("Also click the left and right mouse button event: define it yourself")
Print("Click the left and right mouse button")  # response test statement
Elif
event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # Left middle button simultaneously pressed
self.setText("Also click the middle left mouse button event: define it yourself")
Print("Click the left middle button")  # response test statement
Elif
event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  #
self.setText("Also click the middle right mouse button event: define it yourself")
Print("click the middle right button")  # response test statement
elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
     | QtCore.Qt.RightButton:  # Left and right button simultaneously pressed
self.setText("Also click the left mouse button right event: define it yourself")
Print("Click the left and right mouse button")  # response test statement

'''Overload the wheel scrolling event '''


def wheelEvent(self, event):
    # if event.delta() > 0: # Roller up, PyQt4
    # This function has been deprecated, use pixelDelta() or angleDelta() instead.
    Angle = event.angleDelta() / 8  # Returns the QPoint object, the value of the wheel, in 1/8 degrees


angleX = angle.x()  # The distance rolled horizontally (not used here)
angleY = angle.y()  # The distance that is rolled vertically
if angleY > 0:
    self.setText("Scroll up event: define itself")
    Print("mouse wheel scrolling")  # response test statement
Else:  # roll down
self.setText("Scroll down event: define itself")
Print("mouse wheel down")  # response test statement

'''Overload the mouse double click event '''


def mouseDoubieCiickEvent(self, event):
    # if event.buttons () == QtCore.Qt.LeftButton: # Left button pressed
    # self.setText ("Double-click the left mouse button function: define it yourself")
    self.setText("mouse double click event: define itself")


'''Reload the mouse button release event '''


def mouseReleaseEvent(self, event):
    self.setText("mouse release event: define itself")
    Print("mouse release")  # response test statement


'''Reload the mouse movement event '''


def mouseMoveEvent(self, event):
    self.setText("Mouse Move Event: Defining Yourself")
    Print("mouse movement")  # response test statement


# '''Reload the mouse to enter the control event '''
#    def enterEvent(self, event):
#
#
# '''Reload the mouse to leave the control event '''
#    def leaveEvent(self, event):
#


'''Define the main window'''


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.imgLabel = myImgLabel()  # declare imgLabel
        Self.image = QImage()  # declare new img
        If
        self.image.load("image/cc2.png"):  # If the image is loaded, then
        self.imgLabel.setPixmap(QPixmap.fromImage(self.image))  # Display image

    self.gridLayout = QtWidgets.QGridLayout(self)  # Layout settings
    self.gridLayout.addWidget(self.imgLabel, 0, 0, 1, 1)  # comment out these two sentences, no image will be displayed


'''Main function'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())