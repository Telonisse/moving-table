from pyfirmata import Arduino, SERVO
import threading
from time import sleep

# Arduino setup
port = '/dev/ttyACM0'  # Replace with your port
board = Arduino(port)
servo_pin = 9
board.digital[servo_pin].mode = SERVO

# Global flag and thread reference
servo_running = False
servo_thread = None

def on_start():
    """
    Initial setup for the servo. Sets it to 90 degrees.
    """
    print("Initializing servo...")
    board.digital[servo_pin].write(90)  # Set servo to neutral position
    sleep(0.5)  # Allow some time for the servo to reach the position

def run_servo(pin):
    """
    Keeps the servo running at 90 degrees while the global flag `servo_running` is True.
    """
    while servo_running:
        board.digital[pin].write(0)  # Set to 90 degrees (constant forward motion)
        sleep(0.015)

def start_servo():
    """
    Starts the servo in a separate thread.
    """
    global servo_running, servo_thread
    if not servo_running:
        print("Starting servo...")
        servo_running = True
        servo_thread = threading.Thread(target=run_servo, args=(servo_pin,), daemon=True)
        servo_thread.start()
    else:
        print("Servo is already running.")

def stop_servo():
    """
    Stops the servo.
    """
    global servo_running
    if servo_running:
        print("Stopping servo...")
        servo_running = False
        if servo_thread:
            servo_thread.join()  # Wait for the thread to finish
        board.digital[servo_pin].write(90)  # Stop the servo
    else:
        print("Servo is already stopped.")

def servo_control():
    """
    Control loop for starting and stopping the servo based on user input.
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

# Main program
if __name__ == "__main__":
    try:
        on_start()  # Initialize the servo position
        servo_control()
    finally:
        stop_servo()
        board.exit()
        print("Cleaned up and exited.")