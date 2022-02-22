from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class _Bar(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )


    def sizeHint(self):
        return QtCore.QSize(40,120)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('white'))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        # Get current state.
        dial = self.parent()._dial
        vmin, vmax = dial.minimum(), dial.maximum()
        value = dial.value()

        print(f'Value is  = {dial.value()}')

        padding = 10

        # Define our canvas.
        d_height = painter.device().height() - (padding * 2)
        d_width = painter.device().width() - (padding * 2)

        # Draw the bars.
        step_size = d_height / 10
        bar_height = step_size * 0.6
        bar_spacer = step_size * 0.4 / 2

        pc = (value - vmin) / (vmax - vmin)
        n_steps_to_draw = int(pc * 10)

        if(dial.value()<40):
           brush.setColor(QtGui.QColor('green'))
        elif (dial.value()<70):
            brush.setColor(QtGui.QColor('blue'))
        elif (dial.value() <= dial.maximum()):
            brush.setColor(QtGui.QColor('red'))

        for n in range(n_steps_to_draw):
            rect = QtCore.QRect(    # int x, int y, size x , size y
                padding,
                padding + d_height - ((n+1) * step_size) + bar_spacer,
                d_width,
                bar_height
            )
            painter.fillRect(rect, brush)

        painter.end()

    def _trigger_refresh(self):
        self.update()


class PowerBar(QtWidgets.QWidget):

    #Custom Qt Widget to show a power bar and dial.
    #Demonstrating compound and custom-drawn widget.


    def __init__(self, steps=10, *args, **kwargs):
        super(PowerBar, self).__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        self._bar = _Bar()
        layout.addWidget(self._bar)

        self._dial = QtWidgets.QDial()
        self._dial.valueChanged.connect(
           self._bar._trigger_refresh
        )

        layout.addWidget(self._dial)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    volume = PowerBar()
    volume.show()
    app.exec_()
