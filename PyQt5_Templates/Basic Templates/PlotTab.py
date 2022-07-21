from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import serial
import time
import traceback, sys
import serial.tools.list_ports
import datetime
import numpy as np
#from MainTab import MainTab
import matplotlib.animation as animation
from matplotlib import style
from drawnow import *
import PlotformYoutube



#style.use('fivethirtyeight')


n_data = 50


class PlotTab(QWidget):
    def __init__(self):
        super().__init__()

        self.PlotTabInitUi()


    def PlotTabInitUi(self):


        self.temp=0
        self.canvas = Canvas(self, width=7, height=4)
        #self.canvas.axes.set.xlim(0,100)

        #axes.set_xlim([xmin, xmax])
        self.canvas.move(50, 40)
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 100) for i in range(n_data)]


        self.temp1 = list(range(n_data))

        self.update_plot()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        #self.timer.timeout.connect(self.plo)
        self.timer.start()


        self.Plotbutton = QPushButton("Stop Plotting", self)
        self.Plotbutton.setFixedWidth(75)
        self.Plotbutton.setFixedHeight(40)
        self.Plotbutton.move(100, 450)
        #self.Plotbutton.clicked.connect(self.plo)

        self.PlotTablabel1 = QLabel("0000",self)
        self.PlotTablabel1.move(300 , 500)



    def getval (self, val):
        self.val = int(val)/10

        self.ydata = self.ydata[1:] + [self.val]



    def plo(self):
        """
        print("timer elepsed")
        print(self.xdata)
        print(self.ydata)

        plt.cla()
        plt.plot(self.xdata, self.ydata, 'ro-')

        plt.tight_layout()
        plt.show()


        cnt = cnt + 1

        if (cnt > 20):  # If you have 50 or more points, delete the first one from the array
            cnt = 0
            y_vals.pop(0)  # This allows us to just see the last 50 data points
            x_vals.pop(0)

     
        plt.ylim(0, 100)

        """





    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.ydata = self.ydata[1:] + [random.randint(0, 10)]


        #self.ydata = self.ydata[1:] + [self.temp]  # add to last element of list

        #drawnow(self.makeFig)  # Call drawnow to update our live graph



        #plt.plot(self.ydata, 'ro-')  # plot the temperature

        #plt.legend(loc='upper left')  # plot the legend
        #plt2 = plt.twinx()  # Create a second y axis


        #elf.ydata = self.ydata[1:] + [self.val]  # add to last element of list
       
        self.canvas.axes.cla()  # Clear the canvas.
        self.ydatanew = self.ydata[1:]+[random.randint(0, 1)]

        self.canvas.axes.plot(self.xdata, self.ydata,'ro-')
        #self.canvas.axes.plot(self.xdata, self.ydatanew)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()




class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #axes.set_xlim([xmin,xmax])
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)









