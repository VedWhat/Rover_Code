from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import time,serial
import pyproj#from magneto import get_imu_head
from mag_phone import get_imu_head
g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)

def straight():
    stm_send='m6x4999y0000'
    print ('Going straight')
    ser.write(stm_send.encode())
def anticlockwise():
    stm_send='m3x0000y4999'
    print('Rotating anticlockwise')
    ser.write(stm_send.encode())
def clockwise():
    stm_send='m3x9999y4999'
    print('Rotating clockwise')
    ser.write(stm_send.encode())
def backward():
    stm_send='m6x4999y9999' 
    print('Going backward')
    ser.write(stm_send.encode())
def brute_stop():
    stm_send='m6x4999y4999'
    print('Brute Stop')
    ser.write(stm_send.encode())

def pos_update():
    while True:
        for new_data in gps_socket:
            if new_data:
                    data_stream.unpack(new_data)
                    global latitude,longitude
                    latitude =  data_stream.TPV['lat']
                    longitude =  data_stream.TPV['lon']
                    if (type(latitude)==type('Str')):
                        continue
                    else:
                        current=(latitude,longitude)
                        print(latitude,longitude)
                        return latitude,longitude                           
def get_heading():
    startlong,startlat=pos_update()
    (az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if az12<0:
        az12=az12+360
    return az12,dist
def match_head():
    while True:
        waypoint_heading,dist=get_heading()
        imu_heading=get_imu_head()
        heading_diff=imu_heading-waypoint_heading
        print(imu_heading,waypoint_heading,heading_diff)

        if imu_heading < waypoint_heading+2.5 and imu_heading>waypoint_heading-2.5:
                brute_stop()
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
            waypoint_heading,dist=get_heading()
            if dist>10:
                print('Matching Distance',dist)
                straight()  
            else:
                brute_stop()
                break
        except KeyboardInterrupt:
            brute_stop()
            break
            


global startlat,startlong
global end_latitude,end_longitude
endlat=13.3476049
endlong=74.7920942
matchdist()

