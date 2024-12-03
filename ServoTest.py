from pyfirmata import Arduino, SERVO
from time import sleep
import threading

# Arduino setup
port = '/dev/ttyACM0'  # Replace with your port
board = Arduino(port)
servo_pin = 9
board.digital[servo_pin].mode = SERVO

# Global flag to control the servo
servo_running = False

def rotate_servo_continuous(pin):
    """
    Rotates the servo continuously by sweeping back and forth.
    Runs while the global flag servo_running is True.
    """
    global servo_running
    while servo_running:
        for angle in range(0, 180):
            if not servo_running:
                break
            board.digital[pin].write(angle)
            sleep(0.015)
        for angle in range(180, -1, -1):
            if not servo_running:
                break
            board.digital[pin].write(angle)
            sleep(0.015)

from pyfirmata import Arduino, SERVO
from time import sleep
import threading

# Arduino setup
port = '/dev/ttyACM0'  # Replace with your port
board = Arduino(port)
servo_pin = 9
board.digital[servo_pin].mode = SERVO

# Global flag and thread reference
servo_running = False
servo_thread = None

def rotate_servo_continuous(pin):
    """
    Rotates the servo continuously by sweeping back and forth.
    Runs while the global flag `servo_running` is True.
    """
    while servo_running:
        for angle in range(0, 180):
            if not servo_running:
                break
            board.digital[pin].write(angle)
            sleep(0.015)
        for angle in range(180, -1, -1):
            if not servo_running:
                break
            board.digital[pin].write(angle)
            sleep(0.015)

def start_servo():
    """
    Starts the servo rotation in a separate thread.
    """
    global servo_running, servo_thread
    if not servo_running:
        print("Starting servo...")
        servo_running = True
        servo_thread = threading.Thread(target=rotate_servo_continuous, args=(servo_pin,), daemon=True)
        servo_thread.start()
    else:
        print("Servo is already running.")

def stop_servo():
    """
    Stops the servo rotation.
    """
    global servo_running
    if servo_running:
        print("Stopping servo...")
        servo_running = False
        # Allow the thread to finish before proceeding
        if servo_thread:
            servo_thread.join()
        # Stop the servo by setting it to neutral
        board.digital[servo_pin].write(90)
    else:
        print("Servo is already stopped.")

def servo_control():
    """
    Starts and stops the servo based on user input.
    """
    while True:
        command = input("Enter 'start' to run servo, 'stop' to stop, or 'exit' to quit: ").strip().lower()
        if command == "start":
            start_servo()
        elif command == "stop":
            stop_servo()
        elif command == "exit":
            print("Exiting program...")
            stop_servo()
            break
        else:
            print("Invalid command.")

# Start the control loop
if __name__ == "__main__":
    try:
        servo_control()
    finally:
        stop_servo()
        board.exit()
        print("Cleaned up and exited.")