import socket 
import os 
HOST='127.0.0.1'
PORT1=5008

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT1))
s.listen(1)
conn,address=s.accept()
try:
	while True:
		data=conn.recv(12)
		print("Data:",data)
except:
	s.close()
