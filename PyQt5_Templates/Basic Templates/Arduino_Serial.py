import serial
import time
import io
import threading
import serial.tools.list_ports


Ports = serial.tools.list_ports.comports()
print(Ports[0])
print(Ports[1])




ser = serial.Serial('COM4', 9600, timeout=1)  # ,parity=serial.PARITY_EVEN, rtscts=1)
time.sleep(0.25)
PackLength = 1
ArduinoData1 = [0] * PackLength
ArduinoData2 = [0] * PackLength
DataPacket1 = [0] * 20
numpoints = 40
DataFile = open('DataFile.txt', 'w')

"""
class Arduino_Serial_Data:
    def __init__(self):
        self.ser = serial.Serial('COM4', 9600, timeout=1)  # ,parity=serial.PARITY_EVEN, rtscts=1)
        
    pass
"""



def Print_to_File(data, index):
    # Open File For Writing
    DataFile.write(data)
    if (index % 2 == 0) & (index != 0):
        DataFile.write(',')
    elif index == numpoints:
        DataFile.write('\n')


def Convert_to_String(s):
    # initialization of string to ""xc;
    new = ""

    # traverse in the string
    for x in s:
        new += x

        # return string
    return new


def Convert_to_List(string):
    li = list(string.split(" "))
    return li


def getValues():
    ser.write(b'1')
    ser.flush()
    for j in range(0, PackLength):
        ArduinoData1[j] = ser.readline().decode('ascii').split('\x00')

    ser.write(b'2')
    ser.flush()
    for j in range(0, PackLength):
        ArduinoData2[j] = ser.readline().decode('ascii')  # .split('\x00')

    return (ArduinoData1, ArduinoData2)




while (1):
    userInput = str(input("want to get data from Arduino? : "))
    if userInput == 'y':
        getValues()
        getValues()
        print("\n\r Data Packet 1 = ")
        ArduinoData1_String = Convert_to_String(ArduinoData1[0])
        ArduinoData1_String.split('\r\n')
        ArduinoData1_String.strip()
        ArduinoData1_String_NoWS = ArduinoData1_String.replace(" ", "")

        # Save data to file

        for i in range(0, len(ArduinoData1_String_NoWS)):
            data = ArduinoData1_String_NoWS[i]
            Print_to_File(data, i)

        ArduinoData1_List = Convert_to_List(ArduinoData1_String)
        """ Just some housekeeping stuff """
        for i in range(0, len(ArduinoData1_List)):
            Byte = int(ArduinoData1_List[i], 16)
            DataPacket1[i] = hex(Byte)  # we have our data in HEX format
        print(DataPacket1)
        print("\n\r String Format  =" + ArduinoData1_String)



    elif userInput == 'n':
        ser.close()
        DataFile.close()
        break
