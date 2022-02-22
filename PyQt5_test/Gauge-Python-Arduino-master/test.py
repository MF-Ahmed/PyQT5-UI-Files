import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5 import QtWidgets

class CheckableComboBox(QtWidgets.QComboBox):
    closedPopup = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.setView(QtWidgets.QListView(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

        firstItem = QtGui.QStandardItem("Select Years")
        firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        firstItem.setSelectable(False)
        self.model().appendRow(firstItem)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def checkedItems(self):
        l = []
        for i in range(self.model().rowCount()):
            it = self.model().item(i)
            if it.checkState() == QtCore.Qt.Checked:
                l.append(it.text())
        return l

    def hidePopup(self):
        self.closedPopup.emit()
        super(CheckableComboBox, self).hidePopup()
        QtCore.QTimer.singleShot(0, lambda: self.setCurrentIndex(0))
class Dialog_01(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Title"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.years()
        self.location()
        self.MaxYears()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.listWidget = self.comboBoxv
        self.layout.addWidget(self.listWidget)
        self.listWidget.show()
    def years(self):
        label0 = QLabel('Years', self)
        label0.move(50,50)
        label0.setGeometry(50,50,500,20)

        years = ["2017", "2018", "2019", "2020", "2021", "2022"]
        self.comboBoxv = CheckableComboBox()
        for i, area in enumerate(years):
            item = QtGui.QStandardItem(area)
            item.setCheckable(True)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.comboBoxv.model().appendRow(item)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.listWidget = self.comboBoxv
        self.layout.addWidget(self.listWidget)
        self.listWidget.move(300, 50)


    @QtCore.pyqtSlot()
    def on_closedPopup(self):
        print(len(self.comboBoxv.checkedItems()))


    def location(self):
        label1 = QLabel('Location', self)
        label1.move(50,150)
        label1.setGeometry(50,150,500,20)
        comboBox1 = QComboBox(self)
        for i in range(1,15):
            comboBox1.addItem("LOCATION %i" % i)
        comboBox1.move(300, 150)
        self.locationDrop=comboBox1
    def MaxYears(self):
        label2 = QLabel('Maximum Years', self)
        label2.move(50,250)
        label2.setGeometry(50,250,500,20)
        comboBox2 = QComboBox(self)
        for i in range(1, 10):
            comboBox2.addItem(str(i))
        comboBox2.move(300, 250)
        self.maxyearsDrop=comboBox2

if __name__ == '__main__':

    if not QApplication.instance():
        App = QApplication(sys.argv)
    else:
        App = QApplication.instance()
    ui = Dialog_01()
    ui.show()
    sys.exit(App.exec_())
