from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
from PyQt5.QtCore import QDate
import time
import traceback, sys
import serial.tools.list_ports
import datetime
import images
import logging
from binascii import hexlify
from logging.handlers import TimedRotatingFileHandler
from itertools import count

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done




globalVariable=55

class MainTab(QWidget):



    def __init__(self):
        super().__init__()
        self.FirstTabInitUi()

    def FirstTabInitUi(self):

        self.MaxGauges = 9
        self.MaxLmits = 12
        self.counter = 0
        self.chosenport = 0
        self.PackLength = self.MaxGauges
        self.ArduinoData1 = [0] * self.PackLength
        self.ArduinoLimits = [0] * self.MaxLmits
        self.dummy = [0]*5
        self.PacketCnt = 0
        self.LimitsLength =3
        self.Temp1GetLmtsFlag = 0
        self.Temp2GetLmtsFlag = 0
        self.Press1GetLmtsFlag = 0
        self.Press2GetLmtsFlag = 0
        self.Heater1ONFlag = 0
        self.Heater1OFFFlag = 0

        self.Heater2ONFlag = 0
        self.Heater2OFFFlag = 0

        self.Pump1ONFlag = 0
        self.Pump1OFFFlag = 0


        self.Pump2ONFlag = 0
        self.Pump2OFFFlag = 0

        self.Temp1ReportingFlag = 0
        self.Temp2ReportingFlag = 0
        self.Press1ReportingFlag = 0
        self.Press2ReportingFlag = 0

        self.Heater1StatusUpdFlag = 0
        self.Heater2StatusUpdFlag = 0
        self.Pump1StatusUpdFlag = 0
        self.Pump2StatusUpdFlag = 0

        self.Heater1CurrStatus = 0
        self.Heater1PrevStatus = 0
        self.Heater2CurrStatus = 0
        self.Heater2PrevStatus = 0
        self.Pump1CurrStatus = 0
        self.Pump1PrevStatus = 0
        self.Pump2CurrStatus = 0
        self.Pump2PrevStatus = 0


        self.Temp1ReportingDisableFlag = 0
        self.Temp2ReportingDisableFlag = 0
        self.Press1ReportingDisableFlag = 0
        self.Press2ReportingDisableFlag = 0

        self.Temp1UpdLmtsFlag = 0
        self.Temp2UpdLmtsFlag = 0
        self.Press1UpdLmtsFlag = 0
        self.Press2UpdLmtsFlag = 0
        self.templimts = [0]*10


        self.CommgroupBoxxpos = 20
        self.CommgroupBoxypos = 10
        self.CommgroupBoxwidth = 300
        self.CommgroupBoxheight = 90

        self.ValuesgroupBoxxpos = 20
        self.ValuesgroupBoxypos = 120
        self.ValuesgroupBoxwidth = 370
        self.ValuesgroupBoxheight = 350

        self.LCDSetMaxHeight = 90
        self.LCDSetMaxWidth = 160

        self.LabelNSetMaxHeight = 30
        self.LabelNSetMaxWidth = 45

        self.Stat_CmdgroupBoxposx = 455
        self.Stat_CmdgroupBoxposy = 10
        self.Stat_CmdgroupBoxwidth = 200
        self.Stat_CmdgroupBoxheight = 510

        self.UpdlmtsgroupBoxposx = 675
        self.UpdlmtsgroupBoxposy = 10
        self.UpdlmtsgroupBoxwidth = 250
        self.UpdlmtsgroupBoxheight = 510


        self.msg1 = QMessageBox()
        self.msg1.setIcon(QMessageBox.Critical)
        self.msg1.setWindowTitle("Error")

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        #self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        self.formatter = logging.Formatter("%(asctime)s - %(message)s",
                                           datefmt='%d-%b-%y %H:%M:%S')


        self.handler = TimedRotatingFileHandler('log/PlantMessages', when="midnight", interval=1, encoding='utf8')
        #self.handler = TimedRotatingFileHandler('log/PlantMessages', when="s", interval=10,encoding='utf8')
        #for windows
        self.handler.suffix ="_%#d-%#m-%Y_%H-%M-%S"+".txt"
        # for Pi
        #self.handler.suffix="_%-d-%-m-%Y_%H-%M-%S"+".txt"

        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)



        self.CommgroupBox = QGroupBox("Comunication Settings",self)
        self.CommgroupBox.setGeometry(QRect(self.CommgroupBoxxpos, self.CommgroupBoxypos, self.CommgroupBoxwidth, self.CommgroupBoxheight))

        self.SelectCOM = QLabel("Select COM Port",self.CommgroupBox)
        self.SelectCOM.move(10, 17)

        self.SelectBR = QLabel("Select BR", self.CommgroupBox)
        self.SelectBR.move(10+100+10, 17)

        self.SelectCOM = QComboBox(self.CommgroupBox)
        #self.Combo1.setGeometry(QRect(self.CommgroupBoxxpos+2, self.CommgroupBoxypos+30, 70, 23))
        self.SelectCOM.move(10, 40)
        self.SelectCOM.setFixedWidth(100)

        self.SelectBR = QComboBox(self.CommgroupBox)
        self.SelectBR.move(10+100+10, 40)
        self.SelectBR.setFixedWidth(70)
        self.SelectBR.addItems(['9600','19200','115200'])
        self.index = self.SelectBR.findText('19200')
        self.SelectBR.setCurrentIndex(self.index)

        self.ConDisButton = QPushButton("Connect", self.CommgroupBox)
        self.ConDisButton.move(10 + 100 + 100, 40)
        self.ConDisButton.setCheckable(True)
        self.ConDisButton.clicked[bool].connect(self.press)

        self.CommSettings = QLabel("Select COM, BR",self.CommgroupBox)
        self.CommSettings.move(170 , 17)
        self.CommSettings.setFixedWidth(180)

        self.progressbar = QProgressBar(self.CommgroupBox)
        self.progressbar.setMaximum(100)
        self.progressbar.move(10, 65)
        self.progressbar.setFixedWidth(50*5)


        self.ValuesgroupBox = QGroupBox("Temperature & Pressure Readings",self)
        self.ValuesgroupBox.setGeometry(QRect(self.ValuesgroupBoxxpos, self.ValuesgroupBoxypos, self.ValuesgroupBoxwidth+20, self.ValuesgroupBoxheight))

        #   self.num11 = MyLCDNumber(10, 50)    Not Working have to see later

        self.Temp1Display()
        self.Temp2Display()
        self.Press1Display()
        self.Press2Display()

        self.StatusDisplay()

        self.LimitsUpdDisplay()

        self.StatusRecieved()


        self.AddSerPorts();
        self.index = self.SelectCOM.findText('COM9')
        self.SelectCOM.setCurrentIndex(self.index)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        #self.timer.start()


    """
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("Left Button Clicked")
        elif QMouseEvent.button() == Qt.RightButton:
            #do what you want here
            print("Right Button Clicked")
    """

    def Temp1Display(self):

        self.Temp1groupBox = QGroupBox("Temperature 1", self)

        self.Temp1groupBox.setGeometry(
            QRect(self.ValuesgroupBoxxpos+10, self.ValuesgroupBoxypos+20, self.ValuesgroupBoxwidth-190,
                  self.ValuesgroupBoxheight-200))

        self.Temperature1Posx = self.ValuesgroupBoxxpos-10
        self.Temperature1Posy = self.ValuesgroupBoxypos-95


        self.Temp1Label = QLabel("Reporting",self.Temp1groupBox)
        self.Temp1Label.move(self.Temperature1Posx, self.Temperature1Posy)


        self.Temp1ReportingE = QRadioButton("Enable", self.Temp1groupBox)
        self.Temp1ReportingE.move(self.Temperature1Posx+52, self.Temperature1Posy)

        self.Temp1ReportingD = QRadioButton("Disable", self.Temp1groupBox)
        self.Temp1ReportingD.move(self.Temperature1Posx+110, self.Temperature1Posy)
        self.Temp1ReportingD.setChecked(True)


        self.Gauge1Value = QLabel("00.0", self.Temp1groupBox)
        self.Gauge1Value.setGeometry(QRect(self.Temperature1Posx, self.Temperature1Posy + 30,
                                    self.LCDSetMaxWidth, self.LCDSetMaxHeight))
        self.Gauge1Value.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 29pt "MS Shell Dlg 2"; ')
        self.Gauge1Value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.Temp1ReportingE.toggled.connect(lambda: self.Reporting("Temp1ReportingE",self.Temp1ReportingE))
        self.Temp1ReportingD.toggled.connect(lambda: self.Reporting("Temp1ReportingD",self.Temp1ReportingD))





        #self.Temp1Dic = {'Temp1N': QLabel("N", self.ValuesgroupBox), 'Temp1W':QLabel("W", self.ValuesgroupBox),'Temp1A': QLabel("A", self.ValuesgroupBox)}

        #self.posxTemp1 = 0
        #for x, y in self.Temp1Dic.items():
            #y.move(self.Temperature1Posx+self.posxTemp1, self.Temperature1Posy+126)
            #y.setMaximumHeight(self.LabelNSetMaxHeight)
            #y.setFixedWidth(self.LabelNSetMaxWidth)
            #y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            #y.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 14pt "MS Shell Dlg 2"; ')
            #self.posxTemp1 +=42

        #self.Temp1N =  self.Temp1Dic.get("Temp1N")
        #self.Temp1W = self.Temp1Dic.get("Temp1W")
        #self.Temp1A = self.Temp1Dic.get("Temp1A")


    def Temp2Display(self):

        self.Temp2groupBox = QGroupBox("Temperature 2", self)

        self.Temp2groupBox.setGeometry(
            QRect(self.ValuesgroupBoxxpos+200, self.ValuesgroupBoxypos+20, self.ValuesgroupBoxwidth-190,
                  self.ValuesgroupBoxheight-200))

        self.Temperature2Posx = self.ValuesgroupBoxxpos-10
        self.Temperature2Posy = self.ValuesgroupBoxypos-95


        self.Temp2Label = QLabel("Reporting",self.Temp2groupBox)
        self.Temp2Label.move(self.Temperature2Posx, self.Temperature2Posy)

        self.Temp2ReportingE = QRadioButton("Enable", self.Temp2groupBox)
        self.Temp2ReportingE.move(self.Temperature2Posx+52, self.Temperature2Posy)

        self.Temp2ReportingD = QRadioButton("Disable", self.Temp2groupBox)
        self.Temp2ReportingD.move(self.Temperature2Posx+110, self.Temperature2Posy)
        self.Temp2ReportingD.setChecked(True)

        self.Gauge2Value = QLabel("00.0", self.Temp2groupBox)
        self.Gauge2Value.setGeometry(QRect(self.Temperature2Posx, self.Temperature2Posy + 30,
                                    self.LCDSetMaxWidth, self.LCDSetMaxHeight))
        self.Gauge2Value.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 29pt "MS Shell Dlg 2"; ')
        self.Gauge2Value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.Temp2ReportingE.toggled.connect(lambda: self.Reporting("Temp2ReportingE",self.Temp2ReportingE))
        self.Temp2ReportingD.toggled.connect(lambda: self.Reporting("Temp2ReportingD",self.Temp2ReportingD))


    def Press1Display(self):

        self.Pres1groupBox = QGroupBox("Pressure 1", self)

        self.Pres1groupBox.setGeometry(
            QRect(self.ValuesgroupBoxxpos+10, self.ValuesgroupBoxypos+180, self.ValuesgroupBoxwidth-190,
                  self.ValuesgroupBoxheight-200))

        self.Pres1Posx = self.ValuesgroupBoxxpos-10
        self.Pres1Posy = self.ValuesgroupBoxypos-95


        self.Pres1Label = QLabel("Reporting",self.Pres1groupBox)
        self.Pres1Label.move(self.Pres1Posx, self.Pres1Posy)


        self.Pres1ReportingE = QRadioButton("Enable", self.Pres1groupBox)
        self.Pres1ReportingE.move(self.Pres1Posx+52, self.Pres1Posy)

        self.Pres1ReportingD = QRadioButton("Disable", self.Pres1groupBox)
        self.Pres1ReportingD.move(self.Pres1Posx+110, self.Pres1Posy)
        self.Pres1ReportingD.setChecked(True)


        self.Gauge3Value = QLabel("00.0", self.Pres1groupBox)
        self.Gauge3Value.setGeometry(QRect(self.Pres1Posx, self.Pres1Posy + 30,
                                    self.LCDSetMaxWidth, self.LCDSetMaxHeight))
        self.Gauge3Value.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 25pt "MS Shell Dlg 2"; ')
        self.Gauge3Value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.Pres1ReportingE.toggled.connect(lambda: self.Reporting("Pres1ReportingE",self.Pres1ReportingE))
        self.Pres1ReportingD.toggled.connect(lambda: self.Reporting("Pres1ReportingD",self.Pres1ReportingD))

    def Press2Display(self):

        self.Pres2groupBox = QGroupBox("Pressure 2", self)

        self.Pres2groupBox.setGeometry(
            QRect(self.ValuesgroupBoxxpos+200, self.ValuesgroupBoxypos+180, self.ValuesgroupBoxwidth-190,
                  self.ValuesgroupBoxheight-200))

        self.Pres2Posx = self.ValuesgroupBoxxpos-10
        self.Pres2Posy = self.ValuesgroupBoxypos-95


        self.Pres2Label = QLabel("Reporting",self.Pres2groupBox)
        self.Pres2Label.move(self.Pres2Posx, self.Pres2Posy)


        self.Pres2ReportingE = QRadioButton("Enable", self.Pres2groupBox)
        self.Pres2ReportingE.move(self.Pres2Posx+52, self.Pres2Posy)

        self.Pres2ReportingD = QRadioButton("Disable", self.Pres2groupBox)
        self.Pres2ReportingD.move(self.Pres2Posx+110, self.Pres2Posy)
        self.Pres2ReportingD.setChecked(True)

        self.Gauge4Value = QLabel("00.0", self.Pres2groupBox)
        self.Gauge4Value.setGeometry(QRect(self.Pres2Posx, self.Pres2Posy + 30,
                                    self.LCDSetMaxWidth, self.LCDSetMaxHeight))
        self.Gauge4Value.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 25pt "MS Shell Dlg 2"; ')
        self.Gauge4Value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.Pres2ReportingE.toggled.connect(lambda: self.Reporting("Pres2ReportingE",self.Pres2ReportingE))
        self.Pres2ReportingD.toggled.connect(lambda: self.Reporting("Pres2ReportingD",self.Pres2ReportingD))


    def StatusDisplay(self):

        self.CmdCkhBoxFlagsDic = {
                                     "Heater1ONFlag":0,"Heater1OFFFlag":0,
                                     "Heater2ONFlag":0,"Heater2OFFFlag":0,
                                     "Pump1ONFlag":0,"Pump1OFFFlag":0,
                                     "Pump2ONFlag":0,"Pump2OFFFlag":0,
                                }

        self.Stat_CmdgroupBox1 = QGroupBox("Heater1 Status/Commands", self)
        self.Stat_CmdgroupBox1.setGeometry(QRect(self.Stat_CmdgroupBoxposx, self.Stat_CmdgroupBoxposy,
                                                self.Stat_CmdgroupBoxwidth-20, self.Stat_CmdgroupBoxheight-380))

        self.Heater1 = QLabel(self.Stat_CmdgroupBox1)

        self.Heater1.setGeometry(QRect(15, 30, 80, 80))
        self.Heater1.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")

        #self.Heater1.setGeometry(QRect(15, 30, 60, 60))
        #self.Heater1.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 20px;")
        self.Heater1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.Heater1.setText("Heater1 \n \n OFF")

        self.Heater1ONCB = QCheckBox("ON",self.Stat_CmdgroupBox1)
        self.Heater1ONCB.setGeometry(QRect(110, 40, 50, 20))



        self.Heater1OFFCB = QCheckBox("OFF",self.Stat_CmdgroupBox1)
        self.Heater1OFFCB.setGeometry(QRect(110, 60, 50, 20))

        self.Heater1CommandButton = QPushButton("EXECUTE", self.Stat_CmdgroupBox1)
        self.Heater1CommandButton.setGeometry(QRect(110, 90, 60, 20))

        self.Heater1CommandButton.clicked.connect(lambda: self.CommandButton("Heater1ONFlag","Heater1OFFFlag","Heater1CommandButton"))

        self.Heater1ONCB.toggled.connect(lambda: self.CmdChecked("Heater1ONFlag",self.Heater1ONCB))

        self.Heater1OFFCB.toggled.connect(lambda: self.CmdChecked("Heater1OFFFlag",self.Heater1OFFCB))


        ################################################################################################################
        self.Stat_CmdgroupBox2 = QGroupBox("Heater2 Status/Commands", self)
        self.Stat_CmdgroupBox2.setGeometry(QRect(self.Stat_CmdgroupBoxposx, self.Stat_CmdgroupBoxposy+140,
                                                self.Stat_CmdgroupBoxwidth-20, self.Stat_CmdgroupBoxheight-380))

        self.Heater2 = QLabel(self.Stat_CmdgroupBox2)

        self.Heater2.setGeometry(QRect(15, 30, 80, 80))
        self.Heater2.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
        self.Heater2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.Heater2.setText("Heater2 \n \n OFF")

        self.Heater2ONCB = QCheckBox("ON",self.Stat_CmdgroupBox2)
        self.Heater2ONCB.setGeometry(QRect(110, 40, 50, 20))

        self.Heater2OFFCB = QCheckBox("OFF",self.Stat_CmdgroupBox2)
        self.Heater2OFFCB.setGeometry(QRect(110, 60, 50, 20))

        self.Heater2CommandButton = QPushButton("EXECUTE", self.Stat_CmdgroupBox2)
        self.Heater2CommandButton.setGeometry(QRect(110, 90, 60, 20))

        self.Heater2CommandButton.clicked.connect(lambda: self.CommandButton("Heater2ONFlag","Heater2OFFFlag","Heater2CommandButton"))

        self.Heater2ONCB.toggled.connect(lambda: self.CmdChecked("Heater2ONFlag",self.Heater2ONCB))

        self.Heater2OFFCB.toggled.connect(lambda: self.CmdChecked("Heater2OFFFlag",self.Heater2OFFCB))

        ################################################################################################################
        self.Stat_CmdgroupBox3 = QGroupBox("Pump1 Status/Commands", self)
        self.Stat_CmdgroupBox3.setGeometry(QRect(self.Stat_CmdgroupBoxposx, self.Stat_CmdgroupBoxposy+280,
                                                self.Stat_CmdgroupBoxwidth-20, self.Stat_CmdgroupBoxheight-380))

        self.Pump1 = QLabel(self.Stat_CmdgroupBox3)

        self.Pump1.setGeometry(QRect(15, 30, 80, 80))
        self.Pump1.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
        self.Pump1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.Pump1.setText("Pump1 \n \n OFF")

        self.Pump1ONCB = QCheckBox("ON",self.Stat_CmdgroupBox3)
        self.Pump1ONCB.setGeometry(QRect(110, 40, 50, 20))

        self.Pump1OFFCB = QCheckBox("OFF",self.Stat_CmdgroupBox3)
        self.Pump1OFFCB.setGeometry(QRect(110, 60, 50, 20))

        self.Pump1CommandButton = QPushButton("EXECUTE", self.Stat_CmdgroupBox3)
        self.Pump1CommandButton.setGeometry(QRect(110, 90, 60, 20))


        self.Pump1CommandButton.clicked.connect(lambda: self.CommandButton("Pump1ONFlag","Pump1OFFFlag","Pump1CommandButton"))

        self.Pump1ONCB.toggled.connect(lambda: self.CmdChecked("Pump1ONFlag",self.Pump1ONCB))

        self.Pump1OFFCB.toggled.connect(lambda: self.CmdChecked("Pump1OFFFlag",self.Pump1OFFCB))


        ################################################################################################################
        self.Stat_CmdgroupBox4 = QGroupBox("Pump2 Status/Commands", self)
        self.Stat_CmdgroupBox4.setGeometry(QRect(self.Stat_CmdgroupBoxposx, self.Stat_CmdgroupBoxposy+410,
                                                self.Stat_CmdgroupBoxwidth-20, self.Stat_CmdgroupBoxheight-380))

        self.Pump2 = QLabel(self.Stat_CmdgroupBox4)

        self.Pump2.setGeometry(QRect(15, 30, 80, 80))
        self.Pump2.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
        self.Pump2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.Pump2.setText("Pump2 \n \n OFF")

        self.Pump2ONCB = QCheckBox("ON",self.Stat_CmdgroupBox4)
        self.Pump2ONCB.setGeometry(QRect(110, 40, 50, 20))

        self.Pump2OFFCB = QCheckBox("OFF",self.Stat_CmdgroupBox4)
        self.Pump2OFFCB.setGeometry(QRect(110, 60, 50, 20))

        self.Pump2CommandButton = QPushButton("EXECUTE", self.Stat_CmdgroupBox4)
        self.Pump2CommandButton.setGeometry(QRect(110, 90, 60, 20))

        self.Pump2CommandButton.clicked.connect(lambda: self.CommandButton("Pump2ONFlag","Pump2OFFFlag","Pump2CommandButton"))
        self.Pump2ONCB.toggled.connect(lambda: self.CmdChecked("Pump2ONFlag",self.Pump2ONCB))
        self.Pump2OFFCB.toggled.connect(lambda: self.CmdChecked("Pump2OFFFlag",self.Pump2OFFCB))



    def LimitsUpdDisplay(self):

        self.updnbuttWidth = 30
        self.updnbuttHeight = 30
        self.updnImgWidth = 31
        self.updnImgHeight = 31
        self.Temp1LimitsA = [0] * self.LimitsLength
        self.Temp2LimitsA = [0] * self.LimitsLength
        self.Press1LimitsA = [0] * self.LimitsLength
        self.Press2LimitsA = [0] * self.LimitsLength

        self.Temp1()
        self.Temp2()

        self.Press1()
        self.Press2()

    def Temp1(self):

        self.UpdlmtsgroupBox = QGroupBox("Update Limits", self)
        self.UpdlmtsgroupBox.setGeometry(QRect(self.UpdlmtsgroupBoxposx-20, self.UpdlmtsgroupBoxposy,
                                                self.UpdlmtsgroupBoxwidth+20, self.UpdlmtsgroupBoxheight))
        self.Temp1lmtsgroupBox = QGroupBox("Temp1 Limits", self)
        self.Temp1lmtsgroupBox.setGeometry(QRect(self.UpdlmtsgroupBoxposx-10, self.UpdlmtsgroupBoxposy+20,
                                                self.UpdlmtsgroupBoxwidth, self.UpdlmtsgroupBoxheight-400))

        self.Temp1Dic = { 'DN1': QPushButton(self.Temp1lmtsgroupBox),'DN2': QPushButton(self.Temp1lmtsgroupBox),
                          'DN3': QPushButton(self.Temp1lmtsgroupBox),'UP1': QPushButton(self.Temp1lmtsgroupBox),
                          'UP2': QPushButton(self.Temp1lmtsgroupBox),'UP3': QPushButton(self.Temp1lmtsgroupBox)}

        posyinc1 = 0
        posyinc2 = 0
        count=0

        for x, y in self.Temp1Dic.items():
            if count<3:
                y.setGeometry(QRect(10, 17+posyinc1, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet("QPushButton {border: none; background-image: url(:/UpdLmts/dnOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/dnON.png)}")
                posyinc1 += 30
            else:
                y.setGeometry(QRect(105, 17+posyinc2, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet("QPushButton {border: none; background-image: url(:/UpdLmts/upOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/upON.png)}")
                posyinc2 += 30
            count = count+1
            y.setContextMenuPolicy(Qt.CustomContextMenu)

        self.Temp1UPN = self.Temp1Dic.get("UP1")
        self.Temp1UPW = self.Temp1Dic.get("UP2")
        self.Temp1UPA = self.Temp1Dic.get("UP3")

        self.Temp1DNN = self.Temp1Dic.get("DN1")
        self.Temp1DNW = self.Temp1Dic.get("DN2")
        self.Temp1DNA = self.Temp1Dic.get("DN3")

        self.Temp1UPN.clicked.connect(lambda: self.IncLmt("UP1N"))
        self.Temp1UPW.clicked.connect(lambda: self.IncLmt("UP1W"))
        self.Temp1UPA.clicked.connect(lambda: self.IncLmt("UP1A"))
        self.Temp1DNN.clicked.connect(lambda: self.IncLmt("DN1N"))
        self.Temp1DNW.clicked.connect(lambda: self.IncLmt("DN1W"))
        self.Temp1DNA.clicked.connect(lambda: self.IncLmt("DN1A"))
        #handle right clicks
        self.Temp1UPN.customContextMenuRequested.connect(lambda: self.handle_right_click("UP1NRC"))
        self.Temp1UPW.customContextMenuRequested.connect(lambda: self.handle_right_click("UP1WRC"))
        self.Temp1UPA.customContextMenuRequested.connect(lambda: self.handle_right_click("UP1ARC"))
        self.Temp1DNN.customContextMenuRequested.connect(lambda: self.handle_right_click("DN1NRC"))
        self.Temp1DNW.customContextMenuRequested.connect(lambda: self.handle_right_click("DN1WRC"))
        self.Temp1DNA.customContextMenuRequested.connect(lambda: self.handle_right_click("DN1ARC"))


        self.Temp1UPDVals = {   "N": QLineEdit("0", self.Temp1lmtsgroupBox),
                                "W": QLineEdit("0", self.Temp1lmtsgroupBox),
                                "A": QLineEdit("0", self.Temp1lmtsgroupBox) }
        posyinc=0
        for x, y in self.Temp1UPDVals.items():
            y.setGeometry(QRect(45, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight+10)
            y.setFixedWidth(self.LabelNSetMaxWidth+10)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setMaxLength(5)
            y.setStyleSheet('background-color: rgb(85, 170, 255);font: 8pt "MS Shell Dlg 2"; ')
            posyinc = posyinc+30

        self.Temp1NLV = self.Temp1UPDVals.get("N")
        self.Temp1WLV = self.Temp1UPDVals.get("W")
        self.Temp1ALV = self.Temp1UPDVals.get("A")

        self.Temp1NLV.returnPressed.connect(lambda: self.LimtsEntered("Temp1NValEntered"))
        self.Temp1WLV.returnPressed.connect(lambda: self.LimtsEntered("Temp1WValEntered"))
        self.Temp1ALV.returnPressed.connect(lambda: self.LimtsEntered("Temp1AValEntered"))

        self.Temp1UPDLabels = { 'N': QLabel("Normal", self.Temp1lmtsgroupBox),
                                'W': QLabel("Warning", self.Temp1lmtsgroupBox),
                                'A': QLabel("Action", self.Temp1lmtsgroupBox)}
        posyinc=0

        for x, y in self.Temp1UPDLabels.items():
            y.setGeometry(QRect(140, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight)
            y.setFixedWidth(self.LabelNSetMaxWidth)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 7pt "MS Shell Dlg 2"; ')
            posyinc = posyinc+30

        self.Temp1Buttons = {"Read": QPushButton("Read",self.Temp1lmtsgroupBox),
                             "Update": QPushButton("Update",self.Temp1lmtsgroupBox),}
        posyinc=0

        for x, y in self.Temp1Buttons.items():
            y.setGeometry(QRect(190, 17 + posyinc , 50, 40))
            y.setStyleSheet("background-color: rgb(117, 255, 67);")
            posyinc = posyinc+45

        self.Temp1GetLmts = self.Temp1Buttons.get("Read")
        self.Temp1UpdLmts = self.Temp1Buttons.get("Update")

        self.Temp1GetLmts.clicked.connect(lambda: self.getlimitsclicked("Temp1GetLmts"))
        self.Temp1UpdLmts.clicked.connect(lambda: self.updlimitsclicked("Temp1UpdLmts"))


    def Temp2(self):


        self.Temp2lmtsgroupBox = QGroupBox("Temp2 Limits", self)
        self.Temp2lmtsgroupBox.setGeometry(QRect(self.UpdlmtsgroupBoxposx - 10, self.UpdlmtsgroupBoxposy + 150,
                                                 self.UpdlmtsgroupBoxwidth, self.UpdlmtsgroupBoxheight - 400))

        self.Temp2Dic = {'DN1': QPushButton(self.Temp2lmtsgroupBox), 'DN2': QPushButton(self.Temp2lmtsgroupBox),
                         'DN3': QPushButton(self.Temp2lmtsgroupBox), 'UP1': QPushButton(self.Temp2lmtsgroupBox),
                         'UP2': QPushButton(self.Temp2lmtsgroupBox), 'UP3': QPushButton(self.Temp2lmtsgroupBox)}

        posyinc1 = 0
        posyinc2 = 0
        count = 0

        for x, y in self.Temp2Dic.items():
            if count < 3:
                y.setGeometry(QRect(10, 17 + posyinc1, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/dnOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/dnON.png)}")
                posyinc1 += 30
            else:
                y.setGeometry(QRect(105, 17 + posyinc2, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/upOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/upON.png)}")
                posyinc2 += 30
            count = count + 1
            y.setContextMenuPolicy(Qt.CustomContextMenu)

        self.Temp2UPN = self.Temp2Dic.get("UP1")
        self.Temp2UPW = self.Temp2Dic.get("UP2")
        self.Temp2UPA = self.Temp2Dic.get("UP3")

        self.Temp2DNN = self.Temp2Dic.get("DN1")
        self.Temp2DNW = self.Temp2Dic.get("DN2")
        self.Temp2DNA = self.Temp2Dic.get("DN3")

        self.Temp2UPN.clicked.connect(lambda: self.IncLmt2("UP2N"))
        self.Temp2UPW.clicked.connect(lambda: self.IncLmt2("UP2W"))
        self.Temp2UPA.clicked.connect(lambda: self.IncLmt2("UP2A"))
        self.Temp2DNN.clicked.connect(lambda: self.IncLmt2("DN2N"))
        self.Temp2DNW.clicked.connect(lambda: self.IncLmt2("DN2W"))
        self.Temp2DNA.clicked.connect(lambda: self.IncLmt2("DN2A"))
        # handle right clicks
        self.Temp2UPN.customContextMenuRequested.connect(lambda: self.handle_right_click2("UP2NRC"))
        self.Temp2UPW.customContextMenuRequested.connect(lambda: self.handle_right_click2("UP2WRC"))
        self.Temp2UPA.customContextMenuRequested.connect(lambda: self.handle_right_click2("UP2ARC"))
        self.Temp2DNN.customContextMenuRequested.connect(lambda: self.handle_right_click2("DN2NRC"))
        self.Temp2DNW.customContextMenuRequested.connect(lambda: self.handle_right_click2("DN2WRC"))
        self.Temp2DNA.customContextMenuRequested.connect(lambda: self.handle_right_click2("DN2ARC"))

        self.Temp2UPDVals = {"N": QLineEdit("0", self.Temp2lmtsgroupBox),
                             "W": QLineEdit("0", self.Temp2lmtsgroupBox),
                             "A": QLineEdit("0", self.Temp2lmtsgroupBox)}
        posyinc = 0
        for x, y in self.Temp2UPDVals.items():
            y.setGeometry(QRect(45, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight + 10)
            y.setFixedWidth(self.LabelNSetMaxWidth + 10)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setMaxLength(5)
            y.setStyleSheet('background-color: rgb(85, 170, 255);font: 8pt "MS Shell Dlg 2"; ')
            posyinc = posyinc + 30

        self.Temp2NLV = self.Temp2UPDVals.get("N")
        self.Temp2WLV = self.Temp2UPDVals.get("W")
        self.Temp2ALV = self.Temp2UPDVals.get("A")

        self.Temp2NLV.returnPressed.connect(lambda: self.LimtsEntered2("Temp2NValEntered"))
        self.Temp2WLV.returnPressed.connect(lambda: self.LimtsEntered2("Temp2WValEntered"))
        self.Temp2ALV.returnPressed.connect(lambda: self.LimtsEntered2("Temp2AValEntered"))

        self.Temp2UPDLabels = {'N': QLabel("Normal", self.Temp2lmtsgroupBox),
                               'W': QLabel("Warning", self.Temp2lmtsgroupBox),
                               'A': QLabel("Action", self.Temp2lmtsgroupBox)}
        posyinc = 0

        for x, y in self.Temp2UPDLabels.items():
            y.setGeometry(QRect(140, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight)
            y.setFixedWidth(self.LabelNSetMaxWidth)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 7pt "MS Shell Dlg 2"; ')
            posyinc = posyinc + 30

        self.Temp2Buttons = {"Read": QPushButton("Read", self.Temp2lmtsgroupBox),
                             "Update": QPushButton("Update", self.Temp2lmtsgroupBox), }
        posyinc = 0

        for x, y in self.Temp2Buttons.items():
            y.setGeometry(QRect(190, 17 + posyinc, 50, 40))
            y.setStyleSheet("background-color: rgb(117, 255, 67);")
            posyinc = posyinc + 45

        self.Temp2GetLmts = self.Temp2Buttons.get("Read")
        self.Temp2UpdLmts = self.Temp2Buttons.get("Update")

        self.Temp2GetLmts.clicked.connect(lambda: self.getlimitsclicked("Temp2GetLmts"))
        self.Temp2UpdLmts.clicked.connect(lambda: self.updlimitsclicked("Temp2UpdLmts"))




    def Press1(self):

        self.Press1lmtsgroupBox = QGroupBox("Pressure1 Limits", self)
        self.Press1lmtsgroupBox.setGeometry(QRect(self.UpdlmtsgroupBoxposx-10, self.UpdlmtsgroupBoxposy+275,
                                                self.UpdlmtsgroupBoxwidth, self.UpdlmtsgroupBoxheight-400))
        self.Press1Dic = {'DN1': QPushButton(self.Press1lmtsgroupBox), 'DN2': QPushButton(self.Press1lmtsgroupBox),
                         'DN3': QPushButton(self.Press1lmtsgroupBox), 'UP1': QPushButton(self.Press1lmtsgroupBox),
                         'UP2': QPushButton(self.Press1lmtsgroupBox), 'UP3': QPushButton(self.Press1lmtsgroupBox)}
        posyinc1 = 0
        posyinc2 = 0
        count = 0

        for x, y in self.Press1Dic.items():
            if count < 3:
                y.setGeometry(QRect(10, 17 + posyinc1, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/dnOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/dnON.png)}")
                posyinc1 += 30
            else:
                y.setGeometry(QRect(105, 17 + posyinc2, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/upOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/upON.png)}")
                posyinc2 += 30
            count = count + 1
            y.setContextMenuPolicy(Qt.CustomContextMenu)

        self.Press1UPN = self.Press1Dic.get("UP1")
        self.Press1UPW = self.Press1Dic.get("UP2")
        self.Press1UPA = self.Press1Dic.get("UP3")

        self.Press1DNN = self.Press1Dic.get("DN1")
        self.Press1DNW = self.Press1Dic.get("DN2")
        self.Press1DNA = self.Press1Dic.get("DN3")

        self.Press1UPN.clicked.connect(lambda: self.IncLmt3("UP1N"))
        self.Press1UPW.clicked.connect(lambda: self.IncLmt3("UP1W"))
        self.Press1UPA.clicked.connect(lambda: self.IncLmt3("UP1A"))
        self.Press1DNN.clicked.connect(lambda: self.IncLmt3("DN1N"))
        self.Press1DNW.clicked.connect(lambda: self.IncLmt3("DN1W"))
        self.Press1DNA.clicked.connect(lambda: self.IncLmt3("DN1A"))
        # handle right clicks
        self.Press1UPN.customContextMenuRequested.connect(lambda: self.handle_right_click3("UP1NRC"))
        self.Press1UPW.customContextMenuRequested.connect(lambda: self.handle_right_click3("UP1WRC"))
        self.Press1UPA.customContextMenuRequested.connect(lambda: self.handle_right_click3("UP1ARC"))
        self.Press1DNN.customContextMenuRequested.connect(lambda: self.handle_right_click3("DN1NRC"))
        self.Press1DNW.customContextMenuRequested.connect(lambda: self.handle_right_click3("DN1WRC"))
        self.Press1DNA.customContextMenuRequested.connect(lambda: self.handle_right_click3("DN1ARC"))

        self.Press1UPDVals = {"N": QLineEdit("0", self.Press1lmtsgroupBox),
                             "W": QLineEdit("0", self.Press1lmtsgroupBox),
                             "A": QLineEdit("0", self.Press1lmtsgroupBox)}
        posyinc = 0
        for x, y in self.Press1UPDVals.items():
            y.setGeometry(QRect(45, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight + 10)
            y.setFixedWidth(self.LabelNSetMaxWidth + 10)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('background-color: rgb(85, 170, 255);font: 7pt "MS Shell Dlg 2"; ')
            y.setReadOnly(True)

            posyinc = posyinc + 30

        self.Press1NLV = self.Press1UPDVals.get("N")
        self.Press1WLV = self.Press1UPDVals.get("W")
        self.Press1ALV = self.Press1UPDVals.get("A")



        self.Press1NLV.returnPressed.connect(lambda: self.LimtsEntered3("Press1NValEntered"))
        self.Press1WLV.returnPressed.connect(lambda: self.LimtsEntered3("Press1WValEntered"))
        self.Press1ALV.returnPressed.connect(lambda: self.LimtsEntered3("Press1AValEntered"))

        self.Press1UPDLabels = {'N': QLabel("Normal", self.Press1lmtsgroupBox),
                               'W': QLabel("Warning", self.Press1lmtsgroupBox),
                               'A': QLabel("Action", self.Press1lmtsgroupBox)}
        posyinc = 0

        for x, y in self.Press1UPDLabels.items():
            y.setGeometry(QRect(140, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight)
            y.setFixedWidth(self.LabelNSetMaxWidth)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 7pt "MS Shell Dlg 2"; ')
            posyinc = posyinc + 30

        self.Press1Buttons = {"Read": QPushButton("Read", self.Press1lmtsgroupBox),
                             "Update": QPushButton("Update", self.Press1lmtsgroupBox), }
        posyinc = 0

        for x, y in self.Press1Buttons.items():
            y.setGeometry(QRect(190, 17 + posyinc, 50, 40))
            y.setStyleSheet("background-color: rgb(117, 255, 67);")
            posyinc = posyinc + 45

        self.Press1GetLmts = self.Press1Buttons.get("Read")
        self.Press1UpdLmts = self.Press1Buttons.get("Update")

        self.Press1GetLmts.clicked.connect(lambda: self.getlimitsclicked("Press1GetLmts"))
        self.Press1UpdLmts.clicked.connect(lambda: self.updlimitsclicked("Press1UpdLmts"))



    def Press2(self):

        self.Press2lmtsgroupBox = QGroupBox("Pressure2 Limits", self)
        self.Press2lmtsgroupBox.setGeometry(QRect(self.UpdlmtsgroupBoxposx - 10, self.UpdlmtsgroupBoxposy + 395,
                                                 self.UpdlmtsgroupBoxwidth, self.UpdlmtsgroupBoxheight - 400))


        self.Press2Dic = {'DN1': QPushButton(self.Press2lmtsgroupBox), 'DN2': QPushButton(self.Press2lmtsgroupBox),
                          'DN3': QPushButton(self.Press2lmtsgroupBox), 'UP1': QPushButton(self.Press2lmtsgroupBox),
                          'UP2': QPushButton(self.Press2lmtsgroupBox), 'UP3': QPushButton(self.Press2lmtsgroupBox)}
        posyinc1 = 0
        posyinc2 = 0
        count = 0

        for x, y in self.Press2Dic.items():
            if count < 3:
                y.setGeometry(QRect(10, 17 + posyinc1, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/dnOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/dnON.png)}")
                posyinc1 += 30
            else:
                y.setGeometry(QRect(105, 17 + posyinc2, self.updnbuttWidth, self.updnbuttHeight))
                y.setMask(QRegion(QRect(0, 0, self.updnImgWidth, self.updnImgHeight), QRegion.Ellipse))
                y.setStyleSheet(
                    "QPushButton {border: none; background-image: url(:/UpdLmts/upOFF.png)}""QPushButton:pressed" "{background-image: url(:/UpdLmts/upON.png)}")
                posyinc2 += 30
            count = count + 1
            y.setContextMenuPolicy(Qt.CustomContextMenu)

        self.Press2UPN = self.Press2Dic.get("UP1")
        self.Press2UPW = self.Press2Dic.get("UP2")
        self.Press2UPA = self.Press2Dic.get("UP3")

        self.Press2DNN = self.Press2Dic.get("DN1")
        self.Press2DNW = self.Press2Dic.get("DN2")
        self.Press2DNA = self.Press2Dic.get("DN3")

        self.Press2UPN.clicked.connect(lambda: self.IncLmt4("UP2N"))
        self.Press2UPW.clicked.connect(lambda: self.IncLmt4("UP2W"))
        self.Press2UPA.clicked.connect(lambda: self.IncLmt4("UP2A"))
        self.Press2DNN.clicked.connect(lambda: self.IncLmt4("DN2N"))
        self.Press2DNW.clicked.connect(lambda: self.IncLmt4("DN2W"))
        self.Press2DNA.clicked.connect(lambda: self.IncLmt4("DN2A"))
        # handle right clicks
        self.Press2UPN.customContextMenuRequested.connect(lambda: self.handle_right_click4("UP2NRC"))
        self.Press2UPW.customContextMenuRequested.connect(lambda: self.handle_right_click4("UP2WRC"))
        self.Press2UPA.customContextMenuRequested.connect(lambda: self.handle_right_click4("UP2ARC"))
        self.Press2DNN.customContextMenuRequested.connect(lambda: self.handle_right_click4("DN2NRC"))
        self.Press2DNW.customContextMenuRequested.connect(lambda: self.handle_right_click4("DN2WRC"))
        self.Press2DNA.customContextMenuRequested.connect(lambda: self.handle_right_click4("DN2ARC"))

        self.Press2UPDVals = {"N": QLineEdit("0", self.Press2lmtsgroupBox),
                              "W": QLineEdit("0", self.Press2lmtsgroupBox),
                              "A": QLineEdit("0", self.Press2lmtsgroupBox)}
        posyinc = 0
        for x, y in self.Press2UPDVals.items():
            y.setGeometry(QRect(45, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight + 10)
            y.setFixedWidth(self.LabelNSetMaxWidth + 10)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('background-color: rgb(85, 170, 255);font: 7pt "MS Shell Dlg 2"; ')
            y.setReadOnly(True)
            posyinc = posyinc + 30

        self.Press2NLV = self.Press2UPDVals.get("N")
        self.Press2WLV = self.Press2UPDVals.get("W")
        self.Press2ALV = self.Press2UPDVals.get("A")

        self.Press2NLV.returnPressed.connect(lambda: self.LimtsEntered4("Press2NValEntered"))
        self.Press2WLV.returnPressed.connect(lambda: self.LimtsEntered4("Press2WValEntered"))
        self.Press2ALV.returnPressed.connect(lambda: self.LimtsEntered4("Press2AValEntered"))

        self.Press2UPDLabels = {'N': QLabel("Normal", self.Press2lmtsgroupBox),
                                'W': QLabel("Warning", self.Press2lmtsgroupBox),
                                'A': QLabel("Action", self.Press2lmtsgroupBox)}
        posyinc = 0

        for x, y in self.Press2UPDLabels.items():
            y.setGeometry(QRect(140, 17 + posyinc, 40, 25))
            y.setMaximumHeight(self.LabelNSetMaxHeight)
            y.setFixedWidth(self.LabelNSetMaxWidth)
            y.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            y.setStyleSheet('border: 2px solid green;background-color: rgb(85, 255, 255);font: 7pt "MS Shell Dlg 2"; ')
            posyinc = posyinc + 30

        self.Press2Buttons = {"Read": QPushButton("Read", self.Press2lmtsgroupBox),
                              "Update": QPushButton("Update", self.Press2lmtsgroupBox), }
        posyinc = 0

        for x, y in self.Press2Buttons.items():
            y.setGeometry(QRect(190, 17 + posyinc, 50, 40))
            y.setStyleSheet("background-color: rgb(117, 255, 67);")
            posyinc = posyinc + 45

        self.Press2GetLmts = self.Press2Buttons.get("Read")
        self.Press2UpdLmts = self.Press2Buttons.get("Update")

        self.Press2GetLmts.clicked.connect(lambda: self.getlimitsclicked("Press2GetLmts"))
        self.Press2UpdLmts.clicked.connect(lambda: self.updlimitsclicked("Press2UpdLmts"))


    def getlimitsclicked(self, text):


        if  self.chosenport!=0:
            if text == "Temp1GetLmts":
                self.Temp1GetLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Temperature 1 Limits Read")
                self.logger.info("[CMD] : " + "Temperature1 Limits Read")
            else:
                self.Temp1GetLmtsFlag = 0

            if text == "Temp2GetLmts":
                self.Temp2GetLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Temperature 2 Limits Read")
                self.logger.info("[CMD] : " + "Temperature2 Limits Read")
            else:
                self.Temp2GetLmtsFlag = 0

            if text == "Press1GetLmts":
                self.Press1GetLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pressure 1 Limits Read")
                self.logger.info("[CMD] : " + "Pressure1 Limits Read")
            else:
                self.Press1GetLmtsFlag = 0

            if text == "Press2GetLmts":
                self.Press2GetLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pressure 2 Limits Read")
                self.logger.info("[CMD] : " + "Pressure2 Limits Read")
            else:
                self.Press2GetLmtsFlag = 0

        else:
            self.logger.error("[CMD] : " + "Attemped to Read limits prior to Open the serial port")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Connect to a Serial Port!")
            msg.setWindowTitle("Error")
            msg.exec_()



    def updlimitsclicked(self, text):
        if  self.chosenport!=0:
            if text == "Temp1UpdLmts":
                self.Temp1UpdLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Temperature 1 Limits Updated")
                self.logger.info("[CMD] : " + "Temperature1 Limits Updated")
            else:
                self.Temp1UpdLmtsFlag = 0

            if text == "Temp2UpdLmts":
                self.Temp2UpdLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Temperature 2 Limits Updated")
                self.logger.info("[CMD] : " + "Temperature2 Limits Updated")
            else:
                self.Temp2UpdLmtsFlag = 0

            if text == "Press1UpdLmts":
                self.Press1UpdLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pressure 1 Limits Updated")
                self.logger.info("[CMD] : " + "Pressure1  Limits Updated")
            else:
                self.Press1UpdLmtsFlag = 0

            if text == "Press2UpdLmts":
                self.Press2UpdLmtsFlag = 1
                self.Command_SentText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] :" + "Pressure 2 Limits Updated")
                self.logger.info("[CMD] : " + "Pressure2  Limits Updated")
            else:
                self.Press2UpdLmtsFlag = 0

        else:
            self.logger.error("[CMD] : " + "Attempted to Update limits without openin a serial Port")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Connect to a Serial Port!")
            msg.setWindowTitle("Error")
            msg.exec_()


    def IncLmt(self, text):
        try:
            if text == "UP1N" or text == "DN1N":
                Temp1=0
                Temp1LimitsAInt = int(self.Temp1LimitsA[0])

                if text == "UP1N":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)

                if Temp1> 999  or  Temp1< -999:
                    raise TypeError

                self.Temp1LimitsA[0] = str(Temp1)
                Temp1Str = str(Temp1/10)
                self.Temp1NLV.setText(Temp1Str)
                self.Temp1NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1W" or text == "DN1W":
                Temp1=0
                Temp1LimitsAInt = int(self.Temp1LimitsA[1])
                if text == "UP1W":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)
                if Temp1> 999  or  Temp1< -999:
                    raise TypeError

                self.Temp1LimitsA[1] = str(Temp1)
                Temp1Str = str(Temp1/10)
                self.Temp1WLV.setText(Temp1Str)
                self.Temp1WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1A" or text == "DN1A":
                Temp1=0
                Temp1LimitsAInt = int(self.Temp1LimitsA[2])
                if text == "UP1A":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)
                if Temp1> 999 or  Temp1< -999:
                    raise TypeError

                self.Temp1LimitsA[2] = str(Temp1)
                Temp1Str = str(Temp1/10)
                self.Temp1ALV.setText(Temp1Str)
                self.Temp1ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()



    def IncLmt2(self, text):
        try:
            if text == "UP2N" or text == "DN2N":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[0])
                if text == "UP2N":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)
                if Temp1> 999 or  Temp1< -999:
                    raise TypeError

                self.Temp2LimitsA[0] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp2NLV.setText(Temp1Str)
                self.Temp2NLV.setStyleSheet('background-color: rgb(255, 239, 117)')


            if text == "UP2W" or text == "DN2W":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[1])
                if text == "UP2W":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)
                if Temp1> 999 or  Temp1< -999:
                    raise TypeError

                self.Temp2LimitsA[1] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp2WLV.setText(Temp1Str)
                self.Temp2WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP2A" or text == "DN2A":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[2])
                if text == "UP2A":
                    Temp1 = (Temp1LimitsAInt + 1)
                else:
                    Temp1 = (Temp1LimitsAInt - 1)
                if Temp1> 999 or  Temp1< -999:
                    raise TypeError

                self.Temp2LimitsA[2] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp2ALV.setText(Temp1Str)
                self.Temp2ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()

    def IncLmt3(self, text):

        if text == "UP1N" or text == "DN1N":
            Temp1=0
            Temp1LimitsAInt = int(self.Press1LimitsA[0])
            if text == "UP1N":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press1LimitsA[0] = str(Temp1)
            self.Press1NLV.setText(str(Limit))
            self.Press1NLV.setStyleSheet('background-color: rgb(255, 239, 117)')


        if text == "UP1W" or text == "DN1W":
            Temp1=0
            Temp1LimitsAInt = int(self.Press1LimitsA[1])
            if text == "UP1W":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press1LimitsA[1] = str(Temp1)
            self.Press1WLV.setText(str(Limit))
            self.Press1WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

        if text == "UP1A" or text == "DN1A":
            Temp1=0
            Temp1LimitsAInt = int(self.Press1LimitsA[2])
            if text == "UP1A":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press1LimitsA[2] = str(Temp1)
            self.Press1ALV.setText(str(Limit))
            self.Press1ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

    def IncLmt4(self, text):
        if text == "UP2N" or text == "DN2N":
            Temp1 = 0
            Temp1LimitsAInt = int(self.Press2LimitsA[0])
            if text == "UP2N":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press2LimitsA[0] = str(Temp1)
            self.Press2NLV.setText(str(Limit))
            self.Press2NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

        if text == "UP2W" or text == "DN2W":
            Temp1 = 0
            Temp1LimitsAInt = int(self.Press2LimitsA[1])
            if text == "UP2W":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press2LimitsA[1] = str(Temp1)
            self.Press2WLV.setText(str(Limit))
            #self.Press2WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

        if text == "UP2A" or text == "DN2A":
            Temp1 = 0
            Temp1LimitsAInt = int(self.Press2LimitsA[2])
            if text == "UP2A":
                Temp1 = (Temp1LimitsAInt + 10)
            else:
                Temp1 = (Temp1LimitsAInt - 10)

            LimitF = (float(Temp1)) / 10
            Limit = format(LimitF / 10, "10.1E")

            self.Press2LimitsA[2] = str(Temp1)
            self.Press2ALV.setText(str(Limit))
            self.Press2ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

    def CmdChecked(self,text,ONOFFChkbox):

        if ONOFFChkbox.isChecked() == True:
            if text in self.CmdCkhBoxFlagsDic:
                self.CmdCkhBoxFlagsDic[text] = 1


        else:
            if text in self.CmdCkhBoxFlagsDic:
                self.CmdCkhBoxFlagsDic[text] = 0


    def CommandButton(self, ONFlag, OFFFlag, SourceButton):

        if SourceButton == "Heater1CommandButton":

            if self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.Heater1ONFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S")  +"[CMD] : " + "Heater 1 ON")
                self.logger.info("[CMD] : " + "Heater1 ON")

            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Heater1OFFFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Heater 1 OFF")
                self.logger.info("[CMD] : " + "Heater1 OFF")

            elif self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Heater 1 Invalid Command")
                self.logger.error("[CMD] : " + "Heater1 Invalid Command")
                self.msg1.setText("InValid Command")
                self.msg1.exec_()
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.msg1.setText("Please Select ON or OFF")
                self.msg1.exec_()

        elif SourceButton == "Heater2CommandButton":

            if self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.Heater2ONFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S")  +"[CMD] : " + "Heater 2 ON")
                self.logger.info("[CMD] : " + "Heater2 ON")
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Heater2OFFFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Heater 2 OFF")
                self.logger.info("[CMD] : " + "Heater2 OFF")
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Heater 2 Invalid Command")
                self.msg1.setText("InValid Command")
                self.logger.error("[CMD] : " + "Heater2 Invalid Command")
                self.msg1.exec_()
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.msg1.setText("Please Select ON or OFF")
                self.msg1.exec_()

        elif SourceButton == "Pump1CommandButton":

            if self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.Pump1ONFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S")  +"[CMD] : " + "Pump1 ON")
                self.logger.info("[CMD] : " + "Pump1 ON")

            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Pump1OFFFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pump1 OFF")
                self.logger.info("[CMD] : " + "Pump1 OFF")

            elif self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pump1 Invalid Command")
                self.logger.error("[CMD] : " + "Pump1 Invalid Command")
                self.msg1.setText("InValid Command")
                self.msg1.exec_()
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.msg1.setText("Please Select ON or OFF")
                self.msg1.exec_()

        elif SourceButton == "Pump2CommandButton":

            if self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.Pump2ONFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S")  +"[CMD] : " + "Pump2 ON")
                self.logger.info("[CMD] : " + "Pump2 ON")
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Pump2OFFFlag = 1
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pump2 OFF")
                self.logger.info("[CMD] : " + "Pump2 OFF")
            
            elif self.CmdCkhBoxFlagsDic[ONFlag] == 1 and self.CmdCkhBoxFlagsDic[OFFFlag] == 1:
                self.Command_SentText.append(self.now.strftime("%d-%m-%Y %H:%M:%S") + "[CMD] : " + "Pump2 Invalid Command")
                self.logger.error("[CMD] : " + "Pump2 Invalid Command")
                self.msg1.setText("InValid Command")
                self.msg1.exec_()

            elif self.CmdCkhBoxFlagsDic[ONFlag] == 0 and self.CmdCkhBoxFlagsDic[OFFFlag] == 0:
                self.msg1.setText("Please Select ON or OFF")
                self.msg1.exec_()



    def Btpressed(self,text):
        print("Button Pressed "+text)

    def LimtsEntered(self, text):
        if self.chosenport != 0:
            if text == "Temp1NValEntered":
                try:

                    text = float(self.Temp1NLV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError

                    text = text * 10
                    text = int(text)
                    self.Temp1LimitsA[0] = str(text)
                    self.Temp1NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9")
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()



            if text == "Temp1WValEntered":
                try:
                    text = float(self.Temp1WLV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError
                    text = text * 10
                    text = int(text)
                    self.Temp1LimitsA[1] = str(text)
                    self.Temp1WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9" )
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()

            if text == "Temp1AValEntered":
                # pass
                try:
                    text = float(self.Temp1ALV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError
                    text = text * 10
                    text = int(text)
                    self.Temp1LimitsA[2] = str(text)
                    self.Temp1ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9")
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Connect to a Serial Port!")
            msg.setWindowTitle("Error")
            msg.exec_()


    def LimtsEntered2(self, text):
        if self.chosenport != 0:
            if text == "Temp2NValEntered":
                try:

                    text = float(self.Temp2NLV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError

                    text = text * 10
                    text = int(text)
                    self.Temp2LimitsA[0] = str(text)
                    self.Temp2NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9")
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()



            if text == "Temp2WValEntered":
                try:
                    text = float(self.Temp2WLV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError
                    text = text * 10
                    text = int(text)
                    self.Temp2LimitsA[1] = str(text)
                    self.Temp2WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9" )
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()

            if text == "Temp2AValEntered":
                # pass
                try:
                    text = float(self.Temp2ALV.text())
                    if text>99.9 or text < -99.9:
                        raise TypeError
                    text = text * 10
                    text = int(text)
                    self.Temp2LimitsA[2] = str(text)
                    self.Temp2ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

                except TypeError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Value form -99.9 to 99.9")
                    msg.setWindowTitle("Error")
                    msg.exec_()


                except ValueError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Enter a Numeric Value ")
                    msg.setWindowTitle("Error")
                    msg.exec_()


        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Connect to a Serial Port!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def LimtsEntered3(self, text):
        pass

    def LimtsEntered4(self, text):
        pass


    def handle_right_click(self,text):
        try:
            if text == "UP1NRC" or text == "DN1NRC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp1LimitsA[0])
                if text == "UP1NRC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)
                if Temp1> 999 or Temp1 < -999:
                    raise TypeError

                self.Temp1LimitsA[0] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp1NLV.setText(Temp1Str)
                self.Temp1NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1WRC" or text == "DN1WRC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp1LimitsA[1])
                if text == "UP1WRC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)

                if Temp1> 999 or Temp1 < -999:
                    raise TypeError

                self.Temp1LimitsA[1] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp1WLV.setText(Temp1Str)
                self.Temp1WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1ARC" or text == "DN1ARC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp1LimitsA[2])
                if text == "UP1ARC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)

                if Temp1> 999 or Temp1 < -999:
                    raise TypeError

                self.Temp1LimitsA[2] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp1ALV.setText(Temp1Str)
                self.Temp1ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()


    def handle_right_click2(self,text):
        try:
            if text == "UP2NRC" or text == "DN2NRC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[0])
                if text == "UP2NRC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)
                if Temp1 > 999 or Temp1 < -999:
                    raise TypeError

                self.Temp2LimitsA[0] = str(Temp1)
                Temp2Str = str(Temp1 / 10)
                self.Temp2NLV.setText(Temp2Str)
                self.Temp2NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP2WRC" or text == "DN2WRC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[1])
                if text == "UP2WRC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)
                if Temp1 > 999 or Temp1 < -999:
                    raise TypeError

                self.Temp2LimitsA[1] = str(Temp1)
                Temp2Str = str(Temp1 / 10)
                self.Temp2WLV.setText(Temp2Str)
                self.Temp2WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP2ARC" or text == "DN2ARC":
                Temp1 = 0
                Temp1LimitsAInt = int(self.Temp2LimitsA[2])
                if text == "UP2ARC":
                    Temp1 = (Temp1LimitsAInt + 10)
                else:
                    Temp1 = (Temp1LimitsAInt - 10)

                if Temp1 > 999 or Temp1 < -999:
                    raise TypeError

                self.Temp2LimitsA[2] = str(Temp1)
                Temp1Str = str(Temp1 / 10)
                self.Temp2ALV.setText(Temp1Str)
                self.Temp2ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()


    def handle_right_click3(self,text):
        try:
            if text == "UP1NRC" or text == "DN1NRC":

                LimitsInt = int(self.Press1LimitsA[0])
                if text == "UP1NRC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press1LimitsA[0] = str(Temp1)
                self.Press1NLV.setText(str(Limit))
                self.Press1NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1WRC" or text == "DN1WRC":

                LimitsInt = int(self.Press1LimitsA[1])
                if text == "UP1WRC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press1LimitsA[1] = str(Temp1)
                self.Press1WLV.setText(str(Limit))
                self.Press1WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP1ARC" or text == "DN1ARC":

                LimitsInt = int(self.Press1LimitsA[2])
                if text == "UP1ARC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press1LimitsA[2] = str(Temp1)
                self.Press1ALV.setText(str(Limit))
                self.Press1ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()

    def handle_right_click4(self, text):
        try:
            if text == "UP2NRC" or text == "DN2NRC":

                LimitsInt = int(self.Press2LimitsA[0])
                if text == "UP2NRC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press2LimitsA[0] = str(Temp1)
                self.Press2NLV.setText(str(Limit))
                self.Press2NLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP2WRC" or text == "DN2WRC":

                LimitsInt = int(self.Press2LimitsA[1])
                if text == "UP2WRC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press2LimitsA[1] = str(Temp1)
                self.Press2WLV.setText(str(Limit))
                self.Press2WLV.setStyleSheet('background-color: rgb(255, 239, 117)')

            if text == "UP2ARC" or text == "DN2ARC":

                LimitsInt = int(self.Press2LimitsA[2])
                if text == "UP2ARC":
                    Temp1 = (LimitsInt + 100)
                else:
                    Temp1 = (LimitsInt - 100)

                LimitF = (float(Temp1)) / 10
                Limit = format(LimitF / 10, "10.1E")

                self.Press2LimitsA[2] = str(Temp1)
                self.Press2ALV.setText(str(Limit))
                self.Press2ALV.setStyleSheet('background-color: rgb(255, 239, 117)')

        except TypeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot Exceed MIN and MAX (-99.9 to 99.9)")
            msg.setWindowTitle("Information")
            msg.exec_()









    def StatusRecieved(self):

        self.Status_RecievedBox = QGroupBox("Status Recieved", self)
        self.Status_RecievedBox.setGeometry(QRect(20, 550, 520, 150))

        self.Status_RecievedText = QTextEdit(self.Status_RecievedBox)


        self.Status_RecievedText.setGeometry(QRect(5, 15, 510, 125))
        self.Status_RecievedText.setStyleSheet("font: 12pt \"Comic Sans MS\";\n"
                                    "background-color: rgb(222, 247, 255);")
        self.Status_RecievedText.setReadOnly(True)

        self.Status_RecievedText.verticalScrollBar().rangeChanged.connect(self.change_scroll)
        #self.Status_RecievedText.textChanged.connect(self.textchanged)



        self.Command_SentBox = QGroupBox("Command Sent", self)
        self.Command_SentBox.setGeometry(QRect(550, 550, 375, 150))

        self.Command_SentText = QTextEdit(self.Command_SentBox)

        self.Command_SentText.setGeometry(QRect(5, 15, 365, 125))
        self.Command_SentText.setStyleSheet("font: 9pt \"Comic Sans MS\";\n"
                                    "background-color: rgb(222, 247, 255);")
        self.Command_SentText.setReadOnly(True)
        self.Command_SentText.verticalScrollBar().rangeChanged.connect(self.change_scroll2)


    @pyqtSlot(int, int)
    def change_scroll(self, min, max):
        #print("cambio", min, max)
        self.Status_RecievedText.verticalScrollBar().setSliderPosition(max)

    @pyqtSlot(int, int)
    def change_scroll2(self, min, max):
        #print("cambio", min, max)
        self.Command_SentText.verticalScrollBar().setSliderPosition(max)



    def Reporting (self,text,chkbox):

        if text == "Temp1ReportingE":
            if chkbox.isChecked() == True:
                self.Temp1ReportingFlag = 1
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Temperature 1 Reporting Enabled")
                self.logger.info("[Info] : " + "Temperature1 Reporting Enabled")

        elif text == "Temp1ReportingD":
            if chkbox.isChecked() == True:
                self.Temp1ReportingDisableFlag = 1
                self.Gauge1Value.setStyleSheet(
                    'border: 2px solid green;background-color: rgb(85, 255, 255);font: 29pt "MS Shell Dlg 2"; ')
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Temperature 1 Reporting Disabled")
                self.logger.info("[Info] : " + "Temperature1 Reporting Disabled")

        if text == "Temp2ReportingE":
            if chkbox.isChecked() == True:
                self.Temp2ReportingFlag = 1
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "TempFerature 2 Reporting Enabled")
                self.logger.info("[Info] : " + "Temperature2 Reporting Enabled")

        elif text == "Temp2ReportingD":
            if chkbox.isChecked() == True:
                self.Temp2ReportingDisableFlag = 1
                self.Gauge2Value.setStyleSheet(
                    'border: 2px solid green;background-color: rgb(85, 255, 255);font: 29pt "MS Shell Dlg 2"; ')
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Temperature 2 Reporting Disabled")
                self.logger.info("[Info] : " + "Temperature2 Reporting Disabled")

        if text == "Pres1ReportingE":
            if chkbox.isChecked() == True:
                self.Press1ReportingFlag = 1
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Pressure 1 Reporting Enabled")
                self.logger.info("[Info] : " + "Pressure1 Reporting Enabled")
        elif text == "Pres1ReportingD":
            if chkbox.isChecked() == True:
                self.Press1ReportingDisableFlag = 1
                self.Gauge3Value.setStyleSheet(
                    'border: 2px solid green;background-color: rgb(85, 255, 255);font: 25pt "MS Shell Dlg 2"; ')
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Pressure 2 Reporting Disabled")
                self.logger.info("[Info] : " + "Pressure2 Reporting Disabled")

        if text == "Pres2ReportingE":
            if chkbox.isChecked() == True:
                self.Press2ReportingFlag = 1
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Pressure 2 Reporting Enabled")
                self.logger.info("[Info] : " + "Pressure2 Reporting Enabled")
        elif text == "Pres2ReportingD":
            if chkbox.isChecked() == True:
                self.Press2ReportingDisableFlag = 1
                self.Gauge4Value.setStyleSheet(
                    'border: 2px solid green;background-color: rgb(85, 255, 255);font: 25pt "MS Shell Dlg 2"; ')
                self.Status_RecievedText.append(
                    self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Info] :" + "Pressure 2 Reporting Disabled")
                self.logger.info("[Info] : " + "Pressure2 Reporting Disabled")



    def press (self,pressed):

        if pressed:
            self.chosenport = self.SelectCOM.currentText()
            self.chosenBR = self.SelectBR.currentText()

            if self.chosenport != '':

                print("Connected to " + self.chosenport)
                self.CommSettings.setText("Conncetd to " + self.chosenport)
                self.ConDisButton.setText("Connected")

            worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            # Execute
            self.threadpool.start(worker)

        else:
            if self.chosenport != '':
                self.ConDisButton.setText("Connect")
                #self.chosenport = self.SelectCOM.currentText()
                print("Discon. form " + self.chosenport)
                self.CommSettings.setText("Discon. form " + self.chosenport)
                self.chosenport = 0



    def AddSerPorts(self):
        self.Ports = serial.tools.list_ports.comports()
        for x in range(len(self.Ports)):
            self.Port = self.Ports[x]
            self.Portstr = str(self.Port)
            self.PortName = self.Portstr.split(" ")
            self.portnameA = self.PortName[0]
            self.SelectCOM.addItems([self.portnameA])


    def progress_fn(self, n):

        self.UpdateLCD()
        self.UpdHPStatus()
        self.UpdateLimitsDisp()
        # print("%d%% done" % (n))

        self.progressbar.setValue(n)

    def execute_this_fn(self, progress_callback):

        try:
            self.ser = serial.Serial(self.chosenport, self.chosenBR, timeout=0.4)  # ,parity=serial.PARITY_EVEN, rtscts=1)
            #time.sleep(0.25)

            while (self.chosenport != 0):
                self.now = datetime.datetime.now()

                if self.Temp1ReportingFlag == 1:
                    self.ser.write(bytes(b"temp1stDis                 "))
                if self.Temp2ReportingFlag == 1:
                    self.ser.write(bytes(b"temp2stDis                 "))
                if self.Press1ReportingFlag == 1:
                    self.ser.write(bytes(b"pres1stDis                 "))
                if self.Press2ReportingFlag == 1:
                    self.ser.write(bytes(b"pres2stDis                 "))






                self.ser.write(bytes(b"DataReq                    "))
                #self.ser.write("data\n\r".encode())

                for n in range(0, self.MaxGauges):

                    self.ArduinoData1[n] = self.ser.readline().decode('ascii')
                    self.ArduinoData1[n] = self.ArduinoData1[n].strip('\r\n')

                    if (self.ArduinoData1[n] == ''):
                        self.ArduinoData1[n] = '0'

                    progress_callback.emit(n * 100 / 6)

                    #progress_callback.emit(n * 100 / 4)
                #print("Current date and time : " + self.now.strftime("%Y-%m-%d %H:%M:%S"))
                #print(self.templimts)
                #print(self.ArduinoData1)
                #time.sleep(0.5)
                #time.sleep(0.1)

                if self.Temp1ReportingFlag == 1:
                    self.ser.write(bytes(b"temp1stEn                  "))
                    self.Temp1ReportingFlag = 0

                if self.Temp2ReportingFlag == 1:
                    self.ser.write(bytes(b"temp2stEn                  "))
                    self.Temp2ReportingFlag = 0

                if self.Press1ReportingFlag == 1:
                    self.ser.write(bytes(b"pres1stEn                  "))
                    self.Press1ReportingFlag = 0

                if self.Press2ReportingFlag == 1:
                    self.ser.write(bytes(b"pres2stEn                  "))
                    self.Press2ReportingFlag = 0


                if self.Temp1ReportingDisableFlag == 1:
                    self.ser.write(bytes(b"temp1stDis                 "))
                    self.Temp1ReportingDisableFlag = 0

                    # print("temp1stEn")
                if self.Temp2ReportingDisableFlag == 1:
                    self.ser.write(bytes(b"temp2stDis                 "))
                    self.Temp2ReportingDisableFlag = 0

                if self.Press1ReportingDisableFlag == 1:
                    self.ser.write(bytes(b"pres1stDis                 "))
                    self.Press1ReportingDisableFlag = 0
                if self.Press2ReportingDisableFlag == 1:
                    self.ser.write(bytes(b"pres2stDis                 "))
                    self.Press2ReportingDisableFlag = 0


                if self.Temp1GetLmtsFlag == 1:

                    self.ser.write(bytes(b"GetT1Lm                    "))

                    for n in range(0, 3):
                        self.Temp1LimitsA[n] = self.ser.readline().decode('ascii')
                        self.Temp1LimitsA[n] = self.Temp1LimitsA[n].strip('\r\n')
                        if (self.Temp1LimitsA[n] == ''):
                            self.Temp1LimitsA[n] = '0'


                    self.Temp1NLV.setText(str(float(self.Temp1LimitsA[0]) / 10))
                    self.Temp1WLV.setText(str(float(self.Temp1LimitsA[1]) / 10))
                    self.Temp1ALV.setText(str(float(self.Temp1LimitsA[2]) / 10))
                    self.Temp1NLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Temp1WLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Temp1ALV.setStyleSheet('background-color: rgb(85, 170, 255)')

                    self.Temp1GetLmtsFlag=0

                elif self.Temp2GetLmtsFlag == 1:

                    self.ser.write(bytes(b"GetT2Lm                    "))

                    for n in range(0, 3):
                        self.Temp2LimitsA[n] = self.ser.readline().decode('ascii')
                        self.Temp2LimitsA[n] = self.Temp2LimitsA[n].strip('\r\n')
                        if (self.Temp2LimitsA[n] == ''):
                            self.Temp2LimitsA[n] = '0'

                    self.Temp2NLV.setText(str(float(self.Temp2LimitsA[0]) / 10))
                    self.Temp2WLV.setText(str(float(self.Temp2LimitsA[1]) / 10))
                    self.Temp2ALV.setText(str(float(self.Temp2LimitsA[2]) / 10))
                    self.Temp2NLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Temp2WLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Temp2ALV.setStyleSheet('background-color: rgb(85, 170, 255)')

                    self.Temp2GetLmtsFlag = 0

                elif self.Press1GetLmtsFlag == 1:

                    self.ser.write(bytes(b"GetP1Lm                    "))
                    for n in range(0, 3):
                        self.Press1LimitsA[n] = self.ser.readline().decode('ascii')
                        self.Press1LimitsA[n] = self.Press1LimitsA[n].strip('\r\n')
                        if (self.Press1LimitsA[n] == ''):
                            self.Press1LimitsA[n] = '0'

                    LimitF = (float(self.Press1LimitsA[0])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press1NLV.setText(str(Limit))


                    LimitF = (float(self.Press1LimitsA[1])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press1WLV.setText(str(Limit))

                    LimitF = (float(self.Press1LimitsA[2])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press1ALV.setText(str(Limit))

                    self.Press1NLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Press1WLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Press1ALV.setStyleSheet('background-color: rgb(85, 170, 255)')

                    print(self.Press1LimitsA)


                    self.Press1GetLmtsFlag = 0


                elif self.Press2GetLmtsFlag == 1:
                    self.ser.write(bytes(b"GetP2Lm                    "))
                    for n in range(0, 3):
                        self.Press2LimitsA[n] = self.ser.readline().decode('ascii')
                        self.Press2LimitsA[n] = self.Press2LimitsA[n].strip('\r\n')
                        if (self.Press2LimitsA[n] == ''):
                            self.Press2LimitsA[n] = '0'

                    LimitF = (float(self.Press2LimitsA[0])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press2NLV.setText(str(Limit))

                    LimitF = (float(self.Press2LimitsA[1])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press2WLV.setText(str(Limit))

                    LimitF = (float(self.Press2LimitsA[2])) / 10
                    Limit = format(LimitF / 10, "10.1E")
                    self.Press2ALV.setText(str(Limit))
                    self.Press2NLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Press2WLV.setStyleSheet('background-color: rgb(85, 170, 255)')
                    self.Press2ALV.setStyleSheet('background-color: rgb(85, 170, 255)')

                    self.Press2GetLmtsFlag = 0


                elif self.Temp1UpdLmtsFlag == 1:

                    st1 = "UpdT1Lm"
                    st2 = self.UpdLmts(str(self.Temp1LimitsA[0]))
                    st3 = self.UpdLmts(str(self.Temp1LimitsA[1]))
                    st4 = self.UpdLmts(str(self.Temp1LimitsA[2]))
                    st5 = " 000"
                    st6 = "    "
                    stringtosend = st1+st2+st3+st4+st5+st6
                    self.ser.write(stringtosend.encode())

                    self.Temp1UpdLmtsFlag = 0


                elif self.Temp2UpdLmtsFlag == 1:

                    st1 = "UpdT2Lm"
                    st2 = self.UpdLmts(str(self.Temp2LimitsA[0]))
                    st3 = self.UpdLmts(str(self.Temp2LimitsA[1]))
                    st4 = self.UpdLmts(str(self.Temp2LimitsA[2]))
                    st5 = " 000"
                    st6 = "    "
                    stringtosend = st1+st2+st3+st4+st5+st6
                    self.ser.write(stringtosend.encode())
                    self.Temp2UpdLmtsFlag = 0

                elif self.Press1UpdLmtsFlag == 1:

                    st1 = "UpdP1Lm"
                    st2 = self.UpdLmts(str(self.Press1LimitsA[0]))
                    st3 = self.UpdLmts(str(self.Press1LimitsA[1]))
                    st4 = self.UpdLmts(str(self.Press1LimitsA[2]))
                    st5 = " 000"
                    st6 = "    "
                    stringtosend = st1+st2+st3+st4+st5+st6
                    self.ser.write(stringtosend.encode())
                    self.Press1UpdLmtsFlag = 0

                elif self.Press2UpdLmtsFlag == 1:

                    st1 = "UpdP2Lm"
                    st2 = self.UpdLmts(str(self.Press2LimitsA[0]))
                    st3 = self.UpdLmts(str(self.Press2LimitsA[1]))
                    st4 = self.UpdLmts(str(self.Press2LimitsA[2]))
                    st5 = " 000"
                    st6 = "    "
                    stringtosend = st1+st2+st3+st4+st5+st6
                    self.ser.write(stringtosend.encode())
                    self.Press2UpdLmtsFlag = 0


                if self.Heater1ONFlag == 1:
                    self.ser.write(bytes(b"cmdhea1ON                  "))
                    self.Heater1ONFlag = 0

                elif self.Heater1OFFFlag == 1:
                    self.ser.write(bytes(b"cmdhea1OFF                 "))
                    self.Heater1OFFFlag = 0

                elif self.Heater2ONFlag == 1:
                    self.ser.write(bytes(b"cmdhea2ON                  "))
                    self.Heater2ONFlag = 0

                elif self.Heater2OFFFlag == 1:
                    self.ser.write(bytes(b"cmdhea2OFF                 "))
                    self.Heater2OFFFlag = 0

                elif self.Pump1ONFlag == 1:
                    self.ser.write(bytes(b"cmdpmp1ON                  "))
                    self.Pump1ONFlag = 0

                elif self.Pump1OFFFlag == 1:
                    self.ser.write(bytes(b"cmdpmp1OFF                 "))
                    self.Pump1OFFFlag = 0


                elif self.Pump2ONFlag == 1:
                    self.ser.write(bytes(b"cmdpmp2ON                  "))
                    self.Pump2ONFlag = 0

                elif self.Pump2OFFFlag == 1:
                    self.ser.write(bytes(b"cmdpmp2OFF                 "))
                    self.Pump2OFFFlag = 0

                for i in range(0,1):
                    self.dummy[i] = self.ser.readline().decode('ascii')
                    self.dummy[i] = self.dummy[i].strip('\r\n')
                    self.data = self.dummy[i].split(' ')
                    if (self.dummy[i] == ''):
                        self.dummy[i] = '0'



                if self.data[0] == "Temp1State":
                    if self.data[2] == "Normal":
                        self.Gauge1Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(0, 170, 0);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 1 is at Normal")
                        self.logger.info("[Status] : " + "Temperature1 is at Normal")

                    elif self.data[2] == "Warning":
                        self.Gauge1Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(170, 108, 67);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 1 is at Warning")
                        self.logger.info("[Status] : " + "Temperature1 is at Warning")

                    elif self.data[2] == "Action":
                        self.Gauge1Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(255, 19, 13);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 1 is at Action")
                        self.logger.info("[Status] : " + "Temperature1 is at Action")

                elif self.data[0] == "Temp2State":
                    if self.data[2] == "Normal":
                        self.Gauge2Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(0, 170, 0);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 2 is at Normal")
                        self.logger.info("[Status] : " + "Temperature2 is at Normal")

                    elif self.data[2] == "Warning":
                        self.Gauge2Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(170, 108, 67);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 2 is at Warning")
                        self.logger.info("[Status] : " + "Temperature2 is at Warning")

                    elif self.data[2] == "Action":
                        self.Gauge2Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(255, 19, 13);font: 29pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Temperature 2 is at Action")
                        self.logger.info("[Status] : " + "Temperature2 is at Action")

                elif self.data[0] == "Press1State":
                    if self.data[2] == "Normal":
                        self.Gauge3Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(0, 170, 0);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 1 is at Normal")
                        self.logger.info("[Status] : " + "Pressure1 is at Normal")

                    elif self.data[2] == "Warning":
                        self.Gauge3Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(170, 108, 67);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 1 is at Warning")
                        self.logger.info("[Status] : " + "Pressure1 is at Warning")

                    elif self.data[2] == "Action":
                        self.Gauge3Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(255, 19, 13);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 1 is at Action")
                        self.logger.info("[Status] : " + "Pressure1 is at Action")

                elif self.data[0] == "Press2State":
                    if self.data[2] == "Normal":
                        self.Gauge4Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(0, 170, 0);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 2 is at Normal")
                        self.logger.info("[Status] : " + "Pressure2 is at Normal")

                    elif self.data[2] == "Warning":
                        self.Gauge4Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(170, 108, 67);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 2 is at Warning")
                        self.logger.info("[Status] : " + "Pressure2 is at Warning")

                    elif self.data[2] == "Action":
                        self.Gauge4Value.setStyleSheet(
                            'border: 2px solid green;background-color: rgb(255, 19, 13);font: 25pt "MS Shell Dlg 2"; ')
                        self.Status_RecievedText.append(
                            self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pressure 2 is at Action")
                        self.logger.info("[Status] : " + "Pressure2 is at Action")

                    #time.sleep(0.1)


            print('Port closed')
            self.ser.close()
            for i in range(0, self.MaxGauges):
                self.ArduinoData1[i] = '00.0';
            self.PacketCnt = 0
            return ("Done.", self.ArduinoData1)

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Select a Serial Port!")
            msg.setWindowTitle("Error")
            msg.exec_()
            print("Exception has occured")



    def print_output(self, s):
        pass
        #print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        #self.UpdateLCD()

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)

    def UpdateLCD (self):
       try:
        self.Temp1Value = (float(self.ArduinoData1[0]))/10
        self.Gauge1Value.setText(str(self.Temp1Value))

        self.Temp2Value = (float(self.ArduinoData1[1])) / 10
        self.Gauge2Value.setText(str(self.Temp2Value))


        self.Press1Value = (float(self.ArduinoData1[2]))/10
        self.Press1Value = format(self.Press1Value/10, "10.1E")
        self.Gauge3Value.setText(str(self.Press1Value))



        self.Press2Value = (float(self.ArduinoData1[3]))/10
        self.Press2Value = format(self.Press2Value/10, "10.1E")
        self.Gauge4Value.setText(str(self.Press2Value))
       except Exception as ex :
           print(ex)
           #print("Not a numeric value")


    def UpdHPStatus(self):


        if self.ArduinoData1[5] == '1':
            self.Heater1StatusUpdFlag+=1
            if self.Heater1StatusUpdFlag==3:
                self.Heater1.setText("Heater1 \n \n ON")
                self.Heater1.setStyleSheet("background-color: rgb(255, 89, 24);;border: 3px solid blue; border-radius: 30px;")
                self.Heater1CurrStatus = self.ArduinoData1[5]
                if self.Heater1CurrStatus != self.Heater1PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Heater 1 ON")
                    self.logger.info("[Status] : " + "Heater1 ON")
                    self.Heater1PrevStatus = self.Heater1CurrStatus
                self.Heater1StatusUpdFlag=0

        elif self.ArduinoData1[5] == '0':
            self.Heater1StatusUpdFlag += 1
            if self.Heater1StatusUpdFlag == 3:
                self.Heater1.setText("Heater1 \n \n OFF")
                self.Heater1.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
                self.Heater1CurrStatus = self.ArduinoData1[5]
                if self.Heater1CurrStatus != self.Heater1PrevStatus:

                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Heater 1 OFF")
                    self.logger.info("[Status] : " + "Heater1 OFF")
                self.Heater1PrevStatus = self.Heater1CurrStatus
                self.Heater1StatusUpdFlag = 0

        if self.ArduinoData1[6] == '1':
            self.Heater2StatusUpdFlag+=1
            if self.Heater2StatusUpdFlag==3:
                self.Heater2.setText("Heater2 \n \n ON")
                self.Heater2.setStyleSheet("background-color: rgb(255, 89, 24);;border: 3px solid blue; border-radius: 30px;")
                self.Heater2CurrStatus = self.ArduinoData1[6]
                if self.Heater2CurrStatus != self.Heater2PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Heater 2 ON")
                    self.logger.info("[Status] : " + "Heater2 ON")
                    self.Heater2PrevStatus = self.Heater2CurrStatus
                self.Heater2StatusUpdFlag=0

        elif self.ArduinoData1[6] == '0':
            self.Heater2StatusUpdFlag += 1
            if self.Heater2StatusUpdFlag == 3:
                self.Heater2.setText("Heater2 \n \n OFF")
                self.Heater2.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
                self.Heater2CurrStatus = self.ArduinoData1[6]
                if self.Heater2CurrStatus != self.Heater2PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Heater 2 OFF")
                    self.logger.info("[Status] : " + "Heater2 OFF")
                self.Heater2PrevStatus = self.Heater2CurrStatus
                self.Heater2StatusUpdFlag = 0

        if self.ArduinoData1[7] == '1':
            self.Pump1StatusUpdFlag+=1
            if self.Pump1StatusUpdFlag==3:
                self.Pump1.setText("Pump1 \n \n ON")
                self.Pump1.setStyleSheet("background-color: rgb(255, 89, 24);;border: 3px solid blue; border-radius: 30px;")
                self.Pump1CurrStatus = self.ArduinoData1[7]
                if self.Pump1CurrStatus != self.Pump1PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pump 1 ON")
                    self.logger.info("[Status] : " + "Pump1 ON")
                    self.Pump1PrevStatus = self.Pump1CurrStatus
                self.Pump1StatusUpdFlag=0

        elif self.ArduinoData1[7] == '0':
            self.Pump1StatusUpdFlag += 1
            if self.Pump1StatusUpdFlag == 3:
                self.Pump1.setText("Pump1 \n \n OFF")
                self.Pump1.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
                self.Pump1CurrStatus = self.ArduinoData1[7]
                if self.Pump1CurrStatus != self.Pump1PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pump 1 OFF")
                    self.logger.info("[Status] : " + "Pump1 OFF")
                self.Pump1PrevStatus = self.Pump1CurrStatus
                self.Pump1StatusUpdFlag = 0


        if self.ArduinoData1[8] == '1':
            self.Pump2StatusUpdFlag+=1
            if self.Pump2StatusUpdFlag==3:
                self.Pump2.setText("Pump2 \n \n ON")
                self.Pump2.setStyleSheet("background-color: rgb(255, 89, 24);;border: 3px solid blue; border-radius: 30px;")
                self.Pump2CurrStatus = self.ArduinoData1[8]
                if self.Pump2CurrStatus != self.Pump2PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pump 2 ON")
                    self.logger.info("[Status] : " + "Pump2 ON")
                    self.Pump2PrevStatus = self.Pump2CurrStatus
                self.Pump2StatusUpdFlag=0

        elif self.ArduinoData1[8] == '0':
            self.Pump2StatusUpdFlag += 1
            if self.Pump2StatusUpdFlag == 3:
                self.Pump2.setText("Pump2 \n \n OFF")
                self.Pump2.setStyleSheet("background-color: rgb(76, 255, 133);;border: 3px solid blue; border-radius: 30px;")
                self.Pump2CurrStatus = self.ArduinoData1[8]
                if self.Pump2CurrStatus != self.Pump2PrevStatus:
                    self.Status_RecievedText.append(
                        self.now.strftime("%d-%m-%Y %H:%M:%S") + "[Status] :" + "Pump 2 OFF")
                    self.logger.info("[Status] : " + "Pump2 OFF")
                self.Pump2PrevStatus = self.Pump2CurrStatus
                self.Pump2StatusUpdFlag = 0

    def UpdateLimitsDisp(self):
        pass

    def UpdLmts(self,val):

        stVal = ""

        if (int(val) <= -100):
            stVal = (val)

        elif ((int(val) < 0)):
            stVal = " " + (val)

        elif (int(val) == 0):
            stVal = " " + " " + " " + (val)

        elif (int(val) < 10):
            stVal = " " + " " + " " + (val)

        elif (int(val) < 100):
            stVal = " " + " " + (val)

        else:
            stVal = " " + (val)


        return stVal






