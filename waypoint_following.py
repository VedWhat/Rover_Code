from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import time,serial
import pyproj
from magneto import get_imu_head
g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)

def straight():
	stm_send='m2x4999y0000'
	#print ('Going straight')
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
	#print('Brute Stop')
	ser.write(stm_send.encode())

def pos_update():
    while True:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                global latitude,longitude
                latitude =  data_stream.TPV['lat']
                longitude =  data_stream.TPV['lon']
                if type(longitude) is type('sdas') or type(latitude) is type('sdas'):
                    continue                 
                #print(latitude,longitude)
                return latitude,longitude
        break        
def get_heading():
    startlat,startlong=pos_update()
    (az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if az12<0:
        az12=az12+360
    return az12, dist
def match_head():
    while True:
        waypoint_heading,dist=get_heading()
        #waypoint_heading_opp=waypoint_heading+180
        imu_heading=get_imu_head()
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)

        if imu_heading < waypoint_heading+10 and imu_heading>waypoint_heading-10:
                #brute_stop()
                break
        if heading_diff >=-180:
                if heading_diff<=0:
                        clockwise()
        if heading_diff <-180:
                anticlockwise()
        if heading_diff>=0:
                if heading_diff<180:
                        turn = 2 
                        anticlockwise()             
        if heading_diff >= 180:
                turn = 1
                clockwise()
def matchdist():
    while True:
        try:
            match_head()
            waypoint_heading,waypoint_dist=get_heading()
            if waypoint_dist>5:
                print('Matching Distance',waypoint_dist)
                straight()  
            else:
                print("Reached,Start looking for marker")
                waypoint_lats,waypoint_long=waypoint_generator()
                for lat,lon in zip(waypoint_lat,waypoint_long):
                    endlat=lat
                    endlong=lon
                brute_stop()  
        except KeyboardInterrupt:
            print("Killed")
            brute_stop()
            break


global startlat,startlong
startlat,startlong=pos_update()
global end_latitude,end_longitude,waypoint_lats,waypoint_long
endlat=13.3478231
endlong=74.7921025
matchdist()

