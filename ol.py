from lidar import get_lidar_data
from time import sleep
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
###############################Global variables############################
global obstacle_distance_1,obstacle_distance_2,obstacle_distance
###########################################################################
def straight():
	stm_send='m2x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m2x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m2x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
def backward():
	stm_send='m2x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m2x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())		
while True:
	if obstacle_distance>200 or obstacle_distance is 1:
		straight()
	elif obstacle_distance>50 and obstacle_distance<=200:
		anticlockwise()
	elif obstacle_distance<50:
		brute_stop()	
