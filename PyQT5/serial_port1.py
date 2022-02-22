#import serial
#ser = serial.Serial('COM4', 9600, timeout=1)#,parity=serial.PARITY_EVEN, rtscts=1)

#def getValues():
#	ser.write(b'g')
#	ArduinoData = ser.readline().decode('ascii')
#	return ArduinoData

#while(1):


userInput = str(input("want to get data from Arduino? : "))
	#if userInput == 'y':
print(userInput)
		#print(getValues())