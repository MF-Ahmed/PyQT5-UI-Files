from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
import time
import traceback, sys
import serial.tools.list_ports
import datetime

from binascii import hexlify
from MainTab import MainTab
from PlotTab import PlotTab
from DataAnalysis import DataAnalysis
from itertools import count
import matplotlib.pyplot as plt



class WorkerSignals2(QObject):
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


class Worker2(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callbaweck function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker2, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals2()

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
        self.initUI()



    def initUI(self):

        self.mainwinxpos = 150
        self.mainwinypos = 120
        self.mainwinwidth = 1000
        self.mainwinheight = 800

        self.tabwidgetxpos = self.mainwinxpos-120
        self.tabwidgetypos = self.mainwinypos-110
        self.tabwidgetwidth =  self.mainwinwidth-50
        self.tabwidgetheight = self.mainwinheight-50

        LoggeddataviewGBposx = 10
        LoggeddataviewGBposy = 20
        LoggeddataviewGBWidth = 545
        LoggeddataviewGBHight = 650


        self.setGeometry(self.mainwinxpos, self.mainwinypos, self.mainwinwidth, self.mainwinheight)
        self.setWindowTitle("Test GUI Ver1.1")



        self.tabwidget = QTabWidget(self)
        self.tabwidget.setGeometry(QRect(self.tabwidgetxpos, self.tabwidgetypos, self.tabwidgetwidth, self.tabwidgetheight))

        self.MainTabObj = MainTab()
        self.DataAnalysis = DataAnalysis(LoggeddataviewGBposx,LoggeddataviewGBposy,LoggeddataviewGBWidth,LoggeddataviewGBHight)

        self.threadpool2 = QThreadPool()
        print("Multithreading2 with maximum %d threads" % self.threadpool2.maxThreadCount())

        self.Plot = PlotTab()

        self.tabwidget.addTab(self.MainTabObj,"Main")
        self.tabwidget.addTab(self.DataAnalysis, "Logged Data Analysis")

        self.tabwidget.setCurrentIndex(1)


        #self.tabwidget.currentChanged.connect(self.TabindexChanged)


        #self.Plot.Plotbutton.clicked.connect(self.Disp)

        #self.tabwidget.addTab(ThirdTab(), "Logged Data")
        #self.Plot.Plotbutton.setCheckable(True)
        #self.Plot.Plotbutton.clicked.connect(self.killthread)


        #firstTab.line.textChanged.connect(secondTab.editor.setPlainText)

    def TabindexChanged(self,n):
        print(f'Tab {n} is selected')
        self.graph(n)

    def killthread(self):
        #self.threadactive = False
        #self.wait()
        #for task in self.threads:
            #print(task)
        self.pressed=0
        print("How to kill this thread")
        #self.threadpool2.destroyed()



    def graph(self,pressed):
        self.pressed = pressed
        print(pressed)
        #print(self.threadactive)

        if self.pressed  == 1:
            worker2 = Worker2(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
            worker2.signals.result.connect(self.print_output)
            worker2.signals.finished.connect(self.thread_complete)
            worker2.signals.progress.connect(self.progress_fn2)

            # Execute
            self.threadpool2.start(worker2)

        else:
            self.pressed =0
            #self.threadactive = False
            #self.wait()

        #self.data = self.MainTabObj.ArduinoData1

        #self.Plot.fromtab1.setText(str(self.data[0]))
        #print(self.data)

    def print_output(self, s):
        pass
        #print(s)

    def thread_complete(self):
        print("THREAD 2 COMPLETE!")
        #self.UpdateLCD()



    def progress_fn2(self,n):
        print("%d%% done" % (n))



    def execute_this_fn(self, progress_callback):
        while self.pressed:
            for n in range (0,5):
                time.sleep(0.1)
                progress_callback.emit(n * 100 / 4)
                self.data = self.MainTabObj.ArduinoData1
                print(self.data[0])
                self.Plot.PlotTablabel1.setText(str(self.data[0]))
                self.Plot.getval(self.data[0])



        else:
            return
        print("Thread 2 sleeping")





    def Convert_to_List(self,string):
        li = list(string.split(" "))
        return li


    def Convert_to_String(self,s):
        # initialization of string to ""xc;
        new = ""

        # traverse in the string
        for x in s:
            new += x

            # return string
        return new



    def Print_to_File(self, data, index):
        # Open File For Writing
        self.DataFile.write(data)
        if (index % 2 == 0) & (index != 0):
            self.DataFile.write(',')
        elif index == self.numpoints:
            self.DataFile.write('\n')




if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()