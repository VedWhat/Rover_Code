TCP_IP1   = '127.0.0.1'
TCP_PORT1 = 5008
TCP_PORT2 = 5009
transmit1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit1.connect((TCP_IP1, TCP_PORT1))
transmit2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit2.connect((TCP_IP1, TCP_PORT2))
while True:
	data=transmit1.recv(1)
	data2=transmit2.recv(1)
	if data == 's':
		if data2 == 'a':
			print("Anticlockwise")
		elif data2 == 'c':
			print("Clockwise")
		elif data2 == 'p':
			print("Stop")
		else:
			print("Backward")			 
	else:
		if data2 == 'a':
			print("Anticlockwise")
		elif data2 == 'c':
			print("Clockwise")
		elif data2 == 'p':
			print("Stop")
		else:
			print("Backward")			 	
