from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate
import matplotlib
import os
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import serial
import time
import traceback, sys
import serial.tools.list_ports
import datetime
import numpy as np
# from MainTab import MainTab
import matplotlib.animation as animation
from matplotlib import style
from drawnow import *

import logging
from logging.handlers import TimedRotatingFileHandler






class DataAnalysis(QWidget):
    def __init__(self,LoggeddataviewGBposx,LoggeddataviewGBposy,LoggeddataviewGBWidth,LoggeddataviewGBHight):
        self.LoggeddataviewGBposx = LoggeddataviewGBposx
        self.LoggeddataviewGBposy = LoggeddataviewGBposy
        self.LoggeddataviewGBWidth = LoggeddataviewGBWidth
        self.LoggeddataviewGBHight = LoggeddataviewGBHight

        super().__init__()
        self.DataAnalysis()


    def DataAnalysis(self):
        self.os =os
        self.os.chdir('log')
        self.selectedstartdate=[]
        self.selectedenddate = []
        self.selectedparams = []
        self.selectedmessages = []

        """
        self.formatter = logging.Formatter("%(asctime)s - %(message)s",
                                           datefmt='%d-%b-%y %H:%M:%S')


        #self.handler = TimedRotatingFileHandler('log/PlantMess.log', when="midnight", interval=1, encoding='utf8')
        self.handler = TimedRotatingFileHandler('ErrorLogs', when="s", interval=10,encoding='utf8')
        self.handler.suffix ="_%d-%#m-%Y.txt"
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        """

        datediff=0
        self.LoggeddataviewGB = QGroupBox("Logged Data View", self)
        self.LoggeddataviewGB.setGeometry(QRect(self.LoggeddataviewGBposx , self.LoggeddataviewGBposx,
                                               self.LoggeddataviewGBWidth , self.LoggeddataviewGBHight))

        self.StartDate = QLabel("Select Start date",self.LoggeddataviewGB)
        self.StartDate.move(10,30)
        self.StartDate = QLabel(self.LoggeddataviewGB)
        self.StartDate.setGeometry(QRect(10, 50, 80, 25))
        self.StartDate.setStyleSheet(
            'border: 2px solid green;background-color: rgb(85, 255, 255);font: 10pt "MS Shell Dlg 2"; ')

        self.StartDateButton = QPushButton("Start Date",self.LoggeddataviewGB)
        self.StartDateButton.setGeometry(QRect(100, 50, 80, 25))

        self.EndDate = QLabel("Select End date",self.LoggeddataviewGB)
        self.EndDate.move(190+10,30)
        self.EndDate = QLabel(self.LoggeddataviewGB)
        self.EndDate.setGeometry(QRect(190+10, 50, 80, 25))
        self.EndDate.setStyleSheet(
            'border: 2px solid green;background-color: rgb(85, 255, 255);font: 10pt "MS Shell Dlg 2"; ')

        self.EndDateButton = QPushButton("End Date",self.LoggeddataviewGB)
        self.EndDateButton.setGeometry(QRect(190+100, 50, 80, 25))

        self.SelectParams = QLabel("Select Parameters", self.LoggeddataviewGB)
        self.SelectParams.setGeometry(QRect(190 + 100 + 100+50, 25, 90, 25))
        self.ParamList =  QComboBox(self.LoggeddataviewGB)
        self.ParamList.setGeometry(QRect(190+100+100+40, 50, 100, 25))
        self.ParamList.addItems(['All', 'Temperature1', 'Temperature2','Pressure1', 'Pressure2','Heater1', 'Heater2','Pump1', 'Pump2'])
        self.index = self.ParamList.findText('All')
        self.ParamList.setCurrentIndex(self.index)

        self.SelectMessages = QLabel("Message Type", self.LoggeddataviewGB)
        self.SelectMessages.setGeometry(QRect(10, 90, 90, 25))
        self.MessagesCombo =  QComboBox(self.LoggeddataviewGB)
        self.MessagesCombo.setGeometry(QRect(10, 120, 80, 25))
        self.MessagesCombo.addItems(['All','[Info]','[CMD]','[Status]','[Error]'])
        self.index= self.MessagesCombo.findText('All')
        self.MessagesCombo.setCurrentIndex(self.index)

        self.ViewReportButton = QPushButton("View Report",self.LoggeddataviewGB)
        self.ViewReportButton.setGeometry(QRect(100, 120, 80, 25))


        self.ReportBox = QGroupBox("Logged Data Report", self.LoggeddataviewGB)
        self.ReportBox.setGeometry(QRect(10, 160, 520, 480))

        self.ClearButton = QPushButton("Clear", self.LoggeddataviewGB)
        self.ClearButton.setGeometry(QRect(190 + 100 + 100 + 50, 120, 90, 25))

        self.savetofile = QPushButton("Save to File", self.LoggeddataviewGB)
        self.savetofile.setGeometry(QRect(190, 120, 90, 25))

        self.LoggedReportText = QTextEdit(self.ReportBox)
        self.LoggedReportText.setGeometry(QRect(5, 15, 510, 460))
        self.LoggedReportText.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
                                    "background-color: rgb(222, 247, 255);")
        self.LoggedReportText.setReadOnly(True)

        self.Startdatecalender = QCalendarWidget(self)
        self.Startdatecalender.move(10,30)
        self.Startdatecalender.setVisible(False)
        self.Startdatecalender.setGridVisible(True)

        self.Enddatecalender = QCalendarWidget(self)
        self.Enddatecalender.move(100, 30)
        self.Enddatecalender.setGridVisible(True)
        self.Enddatecalender.setVisible(False)

        self.StartDateButton.clicked.connect(self.StartDateButtonclk)
        self.Startdatecalender.clicked.connect(self.StartDateCalanderclk)

        self.EndDateButton.clicked.connect(self.EndDateButtonclk)
        self.Enddatecalender.clicked.connect(self.EndDateCalanderclk)
        self.ClearButton.clicked.connect(self.ClearButtonClk)
        self.savetofile.clicked.connect(self.savetofileButtonClk)

        self.ViewReportButton.clicked.connect((lambda: self.ViewReport(self.selectedstartdate, self.selectedenddate,
                                                                       self.ParamList.currentText(),
                                                                       self.MessagesCombo.currentText())))

    def StartDateButtonclk(self):
        self.Startdatecalender.setVisible(True)

    def StartDateCalanderclk(self,qdate):

        #print(str(qdate.month()))
        #qdatemonstr = str(qdate.month())
        self.selectedstartdate = '{0}/{1}/{2}'.format(qdate.day(),qdate.month(),qdate.year())
        #print((self.selectedstartdate))
        #print(qdate.toString())
        self.StartDate.setText(self.selectedstartdate)
        self.Startdatecalender.setVisible(False)


    def EndDateButtonclk(self):
        self.Enddatecalender.setVisible(True)

    def EndDateCalanderclk(self,qdate):

        self.selectedenddate = '{0}/{1}/{2}'.format(qdate.day(),qdate.month(),qdate.year())

        self.EndDate.setText(self.selectedenddate)
        self.Enddatecalender.setVisible(False)

    def ClearButtonClk(self):

        self.selectedstartdate=0
        self.selectedenddate=0

        self.LoggedReportText.clear()
        self.StartDate.clear()
        self.EndDate.clear()
        self.Startdatecalender.setVisible(False)
        self.Enddatecalender.setVisible(False)

    def savetofileButtonClk(self):
        # S_File will get the directory path and extension.
        S__File = QFileDialog.getSaveFileName(None, 'SaveTextFile', '/', "Text Files (*.txt)")

        # This will let you access the test in your QTextEdit
        Text = self.LoggedReportText.toPlainText()

        # This will prevent you from an error if pressed cancel on file dialog.
        try:
            if S__File[0]:
                # Finally this will Save your file to the path selected.
                with open(S__File[0], 'w') as file:
                    file.write(Text)
        except Exception as e:
            print(e)

    def ViewReport(self, startdate, enddate, params, messages):
        self.LoggedReportText.clear()
        filedatelist = []
        Startfiletoopenlist =[]
        Startfiletoopendate = []
        Startfiletoopentime =[]
        filetoopen = []
        datediff=0
        
        #print(self.startdate)

        if(startdate == []) or startdate == 0:
            startdate = '00/0/0000'
            self.LoggedReportText.setText("Please Select Appripriate Start Date")

        if(enddate == []) or enddate == 0:
            enddate = '00/0/0000'
            self.LoggedReportText.setText("Please Select Appripriate End Date")


        #try:

        self.startdate = startdate.replace('/', '-')
        self.enddate = enddate.replace('/', '-')
        Startday,Startmonth,Startyear = self.startdate.split('-')
        Endday,Endmonth, Endyear = self.enddate.split('-')
        datediff = int(Endday) - int(Startday)

        if datediff < 0:
            self.LoggedReportText.setText("End date must be equal or greater then Start date")
            filedatelist.append('00-0-0000')



        else:
            for x in range(0, datediff + 1):
                filedatelist.append(str(int(Startday) + x) + '-' + str(Endmonth) + '-' + str(Endyear))

        #print((filedatelist))
        #print(len(filedatelist))
        #except Exception as e:
            #self.logger.error(e,exc_info=True)
        #except Exception as e:
            #print(e)
            #self.LoggedReportText.setText("Please Select Appripriate Dates")


        try:
            count=0
            for f in os.listdir():
                file_name,fileext = os.path.splitext(f)
                filename = file_name.split('_')
                count +=1
                if count>1:
                    Startfiletoopendate.append(filename[1])
                    Startfiletoopentime.append(filename[2])

                for x in range(0,len(filedatelist)):
                    for y in range(0,len(Startfiletoopendate)):
                        if filedatelist[x] == Startfiletoopendate[y]:
                            filetoopen.append("PlantMessages._"+str(filedatelist[x])+"_"+str(Startfiletoopentime[y])+".txt")

                        #else:
                            #filetoopen.append(" ")
                filetoopen = list(dict.fromkeys(filetoopen))
                #try:
                    #filetoopen = filetoopen.remove(" ")
                #except:
                    #print("aloo")
            #print(filetoopen)
            if filetoopen == []:
                self.LoggedReportText.setText("No Records found")

        except:
            print("error")

        try:
            #self.LoggedReportText.clear()
            for file in filetoopen:
                Startfile = open(file, 'r')
                for line in Startfile:
                    l = line.rstrip()
                    j = l.split()
                    if messages == 'All' and params == 'All':
                        self.LoggedReportText.append(l)
                    elif messages == 'All' and params != 'All':
                        if params in j:
                            self.LoggedReportText.append(l)
                    elif messages != 'All' and params == 'All':
                        if messages in j:
                            self.LoggedReportText.append(l)

                    elif messages != 'All' and params != 'All':
                        if messages in j and params in j:
                            self.LoggedReportText.append(l)
                Startfile.close()

        except:
            self.LoggedReportText.setText("No Log record found for selected start date")











        #except Exception as exception:
            #self.logger.error(exception, exc_info=True)


        #print(Startfiletoopen)
        #print(Endfiletoopen)


