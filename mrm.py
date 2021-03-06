#!/usr/bin/env python
import socket
import time
import pygame
from pygame import joystick
import math
import serial
from time import sleep
import os
import rospy
from std_msgs.msg import String

    
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def arm():
	
	_1u=j.get_button(6)
	_1d=j.get_button(7)
	_2u=j.get_button(8)
	_2d=j.get_button(9)
	_3u=j.get_button(10)
	_3d=j.get_button(11)
	_4u=j.get_button(4)
	_4d=j.get_button(2)
	_5u=j.get_button(5)
	_5d=j.get_button(3)
	_6u=0
	_6d=0
	pub.publish('n')
	if _1u:
		pub.publish('A')
	elif _1d:
		pub.publish('A')

	elif _2u:
		pub.publish('A')
	elif _2d:
		pub.publish('A')
	elif _3u:
		pub.publish('A')
	elif _3d:
		pub.publish('A')
	elif _4u:
		pub.publish('A')
	elif _4d:
		pub.publish('A')
	elif _5u:
		pub.publish('A')
	elif _5d:
		pub.publish('A')
	elif _6u:
		pub.publish('A')
	elif _6d:
		pub.publish('A')
def motorcode():
	x1=j.get_axis(0)
	y1=j.get_axis(1)
	gear=j.get_axis(3)
	hat=j.get_hat(0)
	
	gear=int(map1(gear,-1.0,1.0,9,0))
	x=map1(x1,-1.0,1.0,0.0,9999)
	y=map1(y1,-1.0,1.0,0.0,9999)

	zero=j.get_axis(2)

	if(zero>0.7):
		x=9999
		y=4999
	elif(zero<-0.7):
		x=0
		y=4999

	if hat[1]==1:
		y=0
	elif hat[1]==-1:
		y=9999
	if hat[0]==1:
		x=9999
	elif hat[0]==-1:
		x=0
	

	x=str(int(x)).zfill(4)
	y=str(int(y)).zfill(4)
	val="m"+str(gear)+"x"+str(x)+"y"+str(y)
	clear = lambda : os.system('tput reset')
	#clear()
	pub.publish(val)
	try:
		transmit.sendto(val,(UDP_IP,UDP_PORT))
	except Exception:
		print ("Couldn't connect to LAN to UART")
		exit(0)
	
	

	
	#print(ser.read())
	#print(ser.read(),ser.read(),ser.read(),ser.read())
	
	#print(ser.read(),ser.read(),ser.read(),ser.read())

count=0
transmit=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#h=socket.gethostbyaddr('192.168.0.3')
#print h
UDP_IP = '192.168.1.7' # this IP of my pc. When I want raspberry pi 2`s as a client, I replace it with its IP '169.254.54.195'
UDP_PORT = 5005




joystick.init()
pygame.display.init()
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    exit(0)
j=joystick.Joystick(0)
j.init()			
adx='a'
ady='b'
switch=True
active=True
while(1):

	pygame.event.pump()
	on=j.get_button(1)
	if on:
		sleep(0.2)
		if j.get_button(1):
			if active==True:
				active=False
				print('Idle')
			else:
				active=True
				print('Active')

	if active:
		change=j.get_button(0)
		if change:
			sleep(0.2)
			if j.get_button(0):
				if switch==True:
					switch=False
					print('Arm')
				else:
					switch=True
					print('Motor')

		if switch:
			motorcode()
		else:
			arm()
