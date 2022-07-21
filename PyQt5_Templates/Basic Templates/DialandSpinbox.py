import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDial, QSpinBox, QLabel)
from PyQt5.QtGui import QFont

#import Arduino_Serial


Dummy = [1,2,3,4,5,6,7,8,9]

class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.resize(800, 600)
		self.f = QFont('', 16)

		self.Label1 = QLabel(self)
		self.Label1.setGeometry(70, 250, 120, 71)
		self.Label1.setObjectName("label")
		self.Label1.setFont(self.f)
		self.Label1.setText("0")


		self.dial = QDial(self)
		self.dial.setGeometry(370, 10, 111, 131)
		self.dial.setNotchesVisible(True)

		self.spinbox = QSpinBox(self)
		self.spinbox.resize(50, 50)
		self.spinbox.move(250, 100)
		self.spinbox.setFont(self.f)



		self.dial.valueChanged.connect(self.spinbox.setValue)
		self.spinbox.valueChanged.connect(self.dial.setValue)
		self.dial.valueChanged.connect(lambda: self.changeval(Dummy))


	def changeval(self, dummy):
		pass
		#self.Label1.setText(Arduino_Serial.ArduinoData1_String[5])
		#dial.valueChanged['int'].connect(lambda: Label1.setNum.Dummy[2])



if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = MainWindow()
	demo.show()
	sys.exit(app.exec_())