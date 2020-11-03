import serial

def checkSerial_ports():
	ports = ['COM%s'%(i+1)for i in range(256)]
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result

class serialPort():
	'''
	Trigger write class for Neuracle devices, details see the instruction of trigger box.
	To use, please figure out which "COM" port is your device's port. For example, if the port
	is COM3, then when initial the class, you need to set the value of portx to "COM3"
	'''

	def __init__(self,portx,bps=115200,timex=1):
		self.portx = portx
		self.bps = bps
		self.timex = timex
		self.mySerial = serial.Serial(port=self.portx,baudrate=self.bps,timeout=self.timex)
		#self.mySerial.bytesize = 8
		#self.mySerial.stopbits = 1
	
	def serialWrite(self,command):
		toSendString = '01E10100'
		b = hex(command)
		hexcommand = str(hex(command))
		if len(hexcommand) == 3:
			hexvalue = hexcommand[2]
			hexcommand = '0'+hexvalue.upper()
		
		else:
			#hexcommand = hexcommand[-1:-2].upper()
			a = hexcommand[2:].upper()
			hexcommand = a
		toSendString += hexcommand
		#self.mySerial.write(str(toSendString).encode("utf-8"))
		#HexArray = [toSendString[i:i+2] for i in range(0, len(toSendString),2)]
		toSendStringHex2Bytes = [int(toSendString[i:i+2],16) for i in range(0, len(toSendString),2)]
		self.mySerial.write(toSendStringHex2Bytes)
	
	def closePort(self):
		if self.mySerial.isOpen():
			self.mySerial.close()