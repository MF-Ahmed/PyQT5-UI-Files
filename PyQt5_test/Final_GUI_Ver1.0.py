from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
import time
import traceback, sys
import serial.tools.list_ports
import datetime

from binascii import hexlify



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

        # Add the callback to our kwargs
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


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.MaxGauges = 4
        self.counter = 0
        self.chosenport = 0
        self.PackLength = self.MaxGauges
        self.ArduinoData1 = [0] * self.PackLength
        self.PacketCnt = 0
        layout = QGridLayout()

        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(100)


        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        self.Button1 = QPushButton("Connect")

        self.Button1.setCheckable(True)

        self.Button1.clicked[bool].connect(self.press)

        #self.Button1.pressed.connect(self.press)
        #if(self.chosenport !=0):
        #self.ser = serial.Serial(self.chosenport, 9600, timeout=1)  # ,parity=serial.PARITY_EVEN, rtscts=1)


        self.Combo1 = QComboBox()
        self.MessageLabel = QLabel("  ")

        self.Gauge1Label = QLabel("Temperature 1")
        self.Gauge1Label.setFont(QFont("sanserif",15))
        self.Gauge1Label.setStyleSheet('color: rgb(0, 0, 127);background-color: rgb(85, 255, 255);')



        self.Gauge2Label = QLabel("Temperature 2")
        self.Gauge2Label.setFont(QFont("sanserif",15))
        self.Gauge2Label.setStyleSheet('color: rgb(0, 0, 127);background-color: rgb(85, 255, 255);')

        self.Gauge3Label = QLabel("Pressure 1")
        self.Gauge3Label.setFont(QFont("sanserif",15))
        self.Gauge3Label.setStyleSheet('color: rgb(0, 0, 127);background-color: rgb(85, 255, 255);')

        self.Gauge4Label = QLabel("Pressure 2")
        self.Gauge4Label.setFont(QFont("sanserif",15))
        self.Gauge4Label.setStyleSheet('color: rgb(0, 0, 127);background-color: rgb(85, 255, 255);')


        self.Gauge1Value = QLCDNumber()
        self.Gauge1Value.setStyleSheet("""QLCDNumber {background-color: yellow;color: black; }""")



        self.Gauge2Value = QLCDNumber()
        self.Gauge2Value.setStyleSheet('background - color: rgb(255, 236, 213);color: rgb(0, 0, 255)')

        self.Gauge3Value = QLCDNumber()
        self.Gauge3Value.setStyleSheet('color: rgb(0, 0, 255);background - color: rgb(255, 236, 213);')

        self.Gauge4Value = QLCDNumber()
        self.Gauge4Value.setStyleSheet('color: rgb(0, 0, 255);background - color: rgb(255, 236, 213);')



        self.AddSerPorts();
        index = self.Combo1.findText('COM4')
        self.Combo1.setCurrentIndex(index)

        #layout.addWidget(self.l)
        #layout.addWidget(b)
        layout.addWidget(self.progressbar)

        layout.addWidget(self.Combo1)
        layout.addWidget(self.Button1)
        layout.addWidget(self.MessageLabel)
        layout.addWidget(self.Gauge1Label)
        layout.addWidget(self.Gauge1Value)
        layout.addWidget(self.Gauge2Label)
        layout.addWidget(self.Gauge2Value)
        layout.addWidget(self.Gauge3Label)
        layout.addWidget(self.Gauge3Value)
        layout.addWidget(self.Gauge4Label)
        layout.addWidget(self.Gauge4Value)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()


    def Convert_to_List(self,string):
        li = list(string.split(" "))
        return li

    def AddSerPorts(self):
        self.Ports = serial.tools.list_ports.comports()
        for x in range(len(self.Ports)):
            self.Port = self.Ports[x]
            self.Portstr = str(self.Port)
            self.PortName = self.Portstr.split(" ")
            self.portnameA = self.PortName[0]
            self.Combo1.addItems([self.portnameA])

    def press (self,pressed):
        #source = self.sender()
        #print(source)
        if pressed:


            self.chosenport = self.Combo1.currentText()
            print("Connected to " + self.chosenport)
            self.MessageLabel.setText("Conncetd to " + self.chosenport)
            self.Button1.setText("Connected")

            worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            # Execute
            self.threadpool.start(worker)




        else:
            self.Button1.setText("Connect")
            self.chosenport = self.Combo1.currentText()
            print("Disconnected form " + self.chosenport)
            self.MessageLabel.setText("Disconnected form " + self.chosenport)
            #with serial.Serial(self.chosenport, 9600, timeout=1)  as ser:
             #   ser.close()
            self.chosenport = 0


        #if source:

        #else:
            #self.Button1.setText("Disconnect")

    def Convert_to_String(self,s):
        # initialization of string to ""xc;
        new = ""

        # traverse in the string
        for x in s:
            new += x

            # return string
        return new

    def UpdateLCD (self):
        self.Gauge1Value.display(str(self.ArduinoData1[0]))
        self.Gauge2Value.display(str(self.ArduinoData1[1]))
        self.Gauge3Value.display(str(self.ArduinoData1[2]))
        self.Gauge4Value.display(str(self.ArduinoData1[3]))



    def progress_fn(self, n):
        self.UpdateLCD()
        #print("%d%% done" % (n))

        self.progressbar.setValue(n)


    def execute_this_fn(self, progress_callback):
        ser = serial.Serial(self.chosenport, 9600, timeout=1)  # ,parity=serial.PARITY_EVEN, rtscts=1)
        time.sleep(0.25)

        #print("here")
        while(self.chosenport !=0):
            #with serial.Serial(self.chosenport, 9600, timeout=1)  as ser:
                now = datetime.datetime.now()
                ser.write(b'1')
                for n in range(0, self.MaxGauges):
                    self.ArduinoData1[n] = ser.readline().decode('ascii')
                    self.ArduinoData1[n] = self.ArduinoData1[n].strip('\r\n')
                    if (self.ArduinoData1[n] == ''):
                        self.ArduinoData1[n] = '0'
                    #t = hexlify(self.ArduinoData1[1])
                    #ArduinoData1_String = str(t)
                    #dd = str(ArduinoData1_String[2:4])
                    #dd1= dd.strip("'")
                    time.sleep(0.1)
                    progress_callback.emit(n * 100 / 3)

                print("Current date and time : " + now.strftime("%Y-%m-%d %H:%M:%S"))

                #hex_value = hex(an_integer)
                #int(ArduinoData1_String[0:4], 2)
                #print(int('bb', 16))

                print(self.ArduinoData1)

        print('Port closed')
        ser.close()
        for i in range(0,self.MaxGauges):
            self.ArduinoData1[i]='0';
        self.PacketCnt=0
        return ("Done.",self.ArduinoData1)



    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.UpdateLCD()



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


def Print_to_File(self, data, index):
    # Open File For Writing
    self.DataFile.write(data)
    if (index % 2 == 0) & (index != 0):
        self.DataFile.write(',')
    elif index == self.numpoints:
        self.DataFile.write('\n')


app = QApplication([])
window = MainWindow()
app.exec_()