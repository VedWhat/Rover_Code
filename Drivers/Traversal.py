import time,serial
import pyproj
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
def straight():
	stm_send='m6x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m3x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m3x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def backward():
	stm_send='m1x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m2x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
