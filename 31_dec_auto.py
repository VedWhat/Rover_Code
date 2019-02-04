from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import time,serial
import pyproj
#########################################Initialising the Serial line and the Gps##################################
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
###################################################################################################################
#########################################Motor controls############################################################
def straight(gear):
	stm_send='m'+gear+'x4999y9999'	
	ser.write(stm_send.encode())
def anticlockwise(gear):
	stm_send='m'+gear+'x4999y9999'	
	ser.write(stm_send.encode())
def clockwise(gear):
	stm_send='m'+gear+'x4999y9999'	
	ser.write(stm_send.encode())
def backward(gear):
	stm_send='m'+gear+'x4999y9999'	
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m4x4999y4999'
	#print('Brute Stop')
	ser.write(stm_send.encode())