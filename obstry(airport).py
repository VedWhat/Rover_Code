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
#############################Lidar functions########################
global dist_left,dist_right
def is_both_clear():
    return dist_left>50 and dist_right>50
def is_right_clear():    
    return dist_left<50 and dist_right>50
def is_left_clear():
    return dist_left>50 and dist_right<50    
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
        count=0
        waypoint_heading,dist=get_heading()
        imu_heading=get_imu_head()
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)

        if imu_heading < waypoint_heading+10 and imu_heading>waypoint_heading-10:
            if count is 1:
                brute_stop()
                break
            else
                break    
        if heading_diff >=-180:
            if heading_diff<=0:
                    clockwise()
                    count=1
        if heading_diff <-180:
            anticlockwise()
            count=1
        if heading_diff>=0:
            if heading_diff<180:
                    turn = 2 
                    anticlockwise()
                    count=1             
        if heading_diff >= 180:
            turn = 1
            clockwise()
            count=1
def traversal():
    try:
        while True:
            match_head()
            waypoint_heading,waypoint_dist=get_heading()
            if is_clear():
                if waypoint_dist>5:
                    print('Matching Distance',waypoint_dist)
                    straight()
                else:
                    print("Reached")
                    brute_stop()
                    break
            else:
                while(not is_clear()):
                    anticlockwise()   
                for i in range(10):
                    straight()             
    except KeyboardInterrupt:
        print("Killed")
        brute_stop()
        break         

def traversal():
    try:
        while True:
            match_head()
            waypoint_heading,waypoint_dist=get_heading()
            if is_clear():
                if waypoint_dist>5:
                    print('Remaining = ',waypoint_dist)
                    straight()
                else:
                    print("Reached at Location")
                    brute_stop()
                    break
            else:
                if is_left_clear():
                    anticlockwise()
                elif is_right_clear():
                    clockwise()              
    except KeyboardInterrupt:
        print("Killed")
        brute_stop()
        break                                   
global startlat,startlong
startlat,startlong=pos_update()
global end_latitude,end_longitude
endlat=13.3478231
endlong=74.7921025
traversal()

