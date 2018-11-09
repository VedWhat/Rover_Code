from pynput import keyboard
import socket
TCP_IP = '192.168.1.7'
TCP_PORT = 5005
BUFFER_SIZE = 1024
transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transmit.connect((TCP_IP, TCP_PORT))
data=''

def on_press(key):
    try:
        if key==keyboard.Key.w :
            data='m4x4999y0000'
        if key==keyboard.Key.s :
            data='m4x9999y9999'
        if key==keyboard.Key.a :
            data='m4x0000y4999'
        if key==keyboard.Key.d :
            data='m4x9999y4999'
        print(data)
        transmit.send(data)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    #print('{0} released'.format(
     #   key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
try:
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    data='m4x4999y4999'
    print(data)
    transmit.send(data)
