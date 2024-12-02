from pyfirmata import Arduino, SERVO
from time import sleep

port = '/dev/ttyACM0' 
board = Arduino(port) 
servo_pin = board.get_pin('d:9:s') # To initialize the pin used 

pin = 9
board.digital[pin].mode = SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

    
while True:
    for i in range(0,180):
        rotateServo(pin, i)
