import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ClickableLabel(QLabel):
    """
        A Label that emits a signal when clicked.
    """

    def __init__(self, *args):
        super().__init__(*args)


    def mousePressEvent(self, event):
        self.action.triggered.emit()

# example
app = QApplication([])
window = QWidget()
layout = QVBoxLayout(window)
labelA = ClickableLabel("Click Me:")
layout.addWidget(labelA)
labelB = QLabel('Here I am.')
layout.addWidget(labelB)
labelB.hide()

action = QAction('Action', labelA)
labelA.action = action

action.triggered.connect(labelB.show)

window.show()
app.exec_()