import keyboard 
#Using module keyboard
while True:
	if keyboard.is_pressed('q'):#if key 'q' is pressed 
		print('You Pressed A Key!')
		break#finishing the loop
	else:
		print('here')
		pass
