from pyfirmata import Arduino, SERVO
from time import sleep

# Arduino setup
port = '/dev/ttyACM0'  # Replace with your port
board = Arduino(port)
servo_pin = 9
board.digital[servo_pin].mode = SERVO

# Servo control state
servo_running = False

def rotate_servo_continuous(pin):
    """
    Continuously rotates the servo back and forth.
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

if __name__ == "__main__":
    try:
        print("Enter 'start' to run servo, 'stop' to stop, or 'exit' to quit.")
        while True:
            command = input("Command: ").strip().lower()
            if command == "start" and not servo_running:
                print("Starting servo...")
                servo_running = True
                rotate_servo_continuous(servo_pin)
            elif command == "stop" and servo_running:
                print("Stopping servo...")
                servo_running = False
                board.digital[servo_pin].write(90)  # Neutral position
            elif command == "exit":
                print("Exiting program...")
                servo_running = False
                board.digital[servo_pin].write(90)
                break
            else:
                print("Invalid or redundant command.")
    finally:
        board.exit()
        print("Cleaned up and exited.")