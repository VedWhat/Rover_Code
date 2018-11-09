import keyboard
import socket
TCP_IP = '192.168.1.7'
TCP_PORT = 5005
BUFFER_SIZE = 1024
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
data=''
while True:
        try:
                if keyboard.is_pressed('w') :
                        data='m4x4999y0000'
                if keyboard.is_pressed('s') :
                        data='m4x9999y9999'
                if keyboard.is_pressed('a') :
                        data='m4x0000y4999'
                if keyboard.is_pressed('d') :
                        data='m4x9999y4999'			
                print(data)	
                transmit.send(data)

        except KeyboardInterrupt:
                data='m4x4999y4999'
                print('Brute stop')
                transmit.send(data)

