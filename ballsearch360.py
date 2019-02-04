from gps3 import gps3
from math import degrees, radians, cos, sin, asin, sqrt
from geopy import distance
from balldetectClient import getball
from LidarClient import getlidar
import time,serial
import pyproj
from magneto import get_imu_head
g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)
global val
val = "NOTFOUND" 
def detect():
        val = getball()
        if(val=="FOUND"):
                brute_stop()
                print(val)
                quit()
def straight():
	stm_send='m6x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m4x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m4x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def clockwise1():
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
    waypoint_heading,dist=get_heading()    
    while True:
        #waypoint_heading_opp=waypoint_heading+180
        imu_heading=get_imu_head()
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)
        detect()
        if imu_heading < waypoint_heading+20 and imu_heading>waypoint_heading-20:
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
            match_head()
            waypoint_heading,waypoint_dist=get_heading()
            if waypoint_dist>3:
                print('Matching Distance',waypoint_dist)
                straight()
                detect()
            else:
                brute_stop()
                break
def obstacle_avoid()
    while l1>1000 and l2>1000:
        if l1<1000 and l2<1000:
            
def traversal():
        try:
            while True:
                l1,l2=getlidar()
                if l1<1000 or l2 <1000:
                    obstacle_avoid(l1,l2)
                else:
                    matchdist()
        except KeyboardInterrupt:
                brute_stop()
                print("Code killed with ^C")                                
def clock_turn():
        h=get_imu_head()
        z=0
        while z-h <90:
                n=get_imu_head()
                if n<h:
                        z=360+n
                else:
                        z=n
                clockwise1()
                val=getball()
                if(val == "FOUND"):
                        brute_stop()
                        print(val,"Ball detected")
                        quit()
def anti_turn():
	h = get_imu_head()
	n = get_imu_head()
	if h>90:
		while abs(h-n)<90:
			anticlockwise()
			n =get_imu_head()
	else:
		while n>=0:
			anticlockwise()
			n=get_imu_head()
		while (360+h-n)<90:
			anticlockwise()
			n=get_imu_head()

def ballsearch():
    print("Ball search starting")
    startlat,startlong=pos_update()
    x = startlat
    y = startlong
    way = []
    r = 6
    for i in range(0, 361, 60):
        cx = cos(radians(i))*r/111035 + x
        cy = sin(radians(i))*r/111035 + y
        a = []
        a.append(cx)
        a.append(cy)
        way.append(a)
        print("way", way)
    for i in range(len(way)):
        for i in range(0,4):
            clock_turn()
        endlat = way[i][0]
        endlong = way[i][1]
        traversal()
        print(i, "REACHED!!!!!!")    

global startlat,startlong
startlat,startlong=pos_update()
global endlat,endlong
endlat=13.3477285
endlong=74.7921968
traversal()
ballsearch()