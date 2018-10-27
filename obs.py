from lidar import get_lidar_data
from time import sleep
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
###############################Global variables############################
global obstacle_distance_1,obstacle_distance_2
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
def is_left_clear():
	return obstacle_distance_1>100
def is_right_clear():
	return obstacle_distance_2>100
def is_both_clear():
	obstacle_distance_1,obstacle_distance_2=get_lidar_data()
	return is_left_clear() && is_right_clear()			
while True:
	if is_both_clear():
		straight()
	elif is_right_clear():
		clockwise()
	elif is_left_clear():
		anticlockwise()
	else:
		brute_stop()
		time.sleep(100)	
		backward()		