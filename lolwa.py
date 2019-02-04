import serial
ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 38400)
stm_send='m2x4999y0000'
#print ('Going straight')
while True:
	ser.write(stm_send.encode())
	print(ser.read())