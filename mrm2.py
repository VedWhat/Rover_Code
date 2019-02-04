import time
import pygame
from pygame import joystick
from time import sleep

flag= True
def irc():
	x1=j.get_axis(0)
	y1=j.get_axis(1)
	gear=j.get_axis(3)
	hat=j.get_hat(0)
	ab="Center"
	abc="t"
	#gear=int(map1(gear,-1.0,1.0,9,0))
	x=x1
	y=-y1
	val="x"+str(x)+"y"+str(y)
	#print (val)
	if abs(x)<=0.9700 and abs(y)<=0.9700:
		#print("Center")
		if a[len(a)-1] != "Center":
			a.append("Center")		
		else:
			pass	
	else:	
		if y>0.9700:
			if abs(x)<=y:
				#print("N")
				if a[len(a)-1] != "N":
					a.append("N")
			else:
				if x>0.9700:
					#print("E")
					if a[len(a)-1] != "E":
						a.append("E")				
				else:
					#print("W")
					if a[len(a)-1] != "W":
						a.append("W")			
		else:
			if abs(x)<=abs(y):
				#print("S")
				if a[len(a)-1] != "S":
					a.append("S")				
			else:
				if x>0.9700:
				#	print("E")	
					if a[len(a)-1] != "E":
						a.append("E")								
				else:
				#	print("W")	
					if a[len(a)-1] != "W":
						a.append("W")			

	print(a)

	if ab in a:
		a.remove(ab)
	if len(a)>=5:
		if a[len(a)-4]=="N" and a[len(a)-3]=="E" and a[len(a)-2]=="S" and a[len(a)-1]=="W":
			print("You win")
			quit()

joystick.init()
pygame.display.init()
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    exit(0)
j=joystick.Joystick(0)
j.init()			
global a
a=list()
a.append("t")

while flag==True:
	st=time.time()
	while time.time()-st<=300:
		pygame.event.pump()
		irc()
		if not flag:
			break
	print("Reset time reached")		
	a[:]=["t"]

	