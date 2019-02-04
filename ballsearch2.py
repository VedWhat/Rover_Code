from gps3 import gps3
from math import degrees, radians, cos, sin, asin, sqrt
from geopy import distance
from balldetectClient import getball
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
	stm_send='m4x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m2x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m2x9999y4999'
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
        try:
            while True:
                match_head()
                waypoint_heading,waypoint_dist=get_heading()
                if waypoint_dist>2:
                    print('Matching Distance',waypoint_dist)
                    straight()  
                else:
                    brute_stop()
                    break
        except KeyboardInterrupt:
                brute_stop()
                
                        


global startlat,startlong
startlat,startlong=pos_update()
global endlat,endlong
endlat=13.3477168      
endlong=74.7921555
matchdist()
print("Ball search starting")
startlat,startlong=pos_update()
x = startlat
y = startlong
way = []
r = 5
val = "NOTFOUND"
ang = 60
# plt.plot(x,y,marker='o',markersize=5, color='red')
while val!= "FOUND":
    for i in range(0, 361, ang):
        cx = cos(degrees(i))*r/111035 + x
        cy = sin(degrees(i))*r/111035 + y
        a = []
        a.append(cx)
        a.append(cy)
        way.append(a)
        print("way", way)
        # plt.plot(cx,cy,marker='o',markersize=3, color='green')
        # plt.draw()
        # plt.pause(0.001)
    for i in range(len(way)):
        endlat = way[i][0]
        endlong = way[i][1]
        matchdist()
        val = getball()
        if(val=='FOUND'):
                break
        print(i, "REACHED!!!!!!")
    r = r*2
    ang = ang/2