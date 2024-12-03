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

def servo_control():
    """
    Starts and stops the servo based on user input.
    """
    global servo_running
    while True:
        command = input("Enter 'start' to run servo, 'stop' to stop, or 'exit' to quit: ").strip().lower()
        if command == "start" and not servo_running:
            print("Starting servo...")
            servo_running = True
            # Run the servo in a separate thread to avoid blocking input
            threading.Thread(target=rotate_servo_continuous, args=(servo_pin,), daemon=True).start()
        elif command == "stop" and servo_running:
            print("Stopping servo...")
            servo_running = False
        elif command == "exit":
            print("Exiting program...")
            servo_running = False
            break
        else:
            print("Invalid command or servo is already in the requested state.")

# Start the control loop
if __name__ == "__main__":
    try:
        servo_control()
    finally:
        board.digital[servo_pin].write(90)  # Neutral position to stop the servo
        board.exit()
        print("Cleaned up and exited.")
