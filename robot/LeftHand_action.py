import serial
import time

# Open a serial connection to the servo controller
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Function to send a command to the servo controller
def send_command(command):
    ser.write((command + '\r\n').encode())  # Add '\r\n' for CRLF
    time.sleep(0.1)  # Short delay to ensure command is sent

# Function to raise both servos (IDs 10 11 and 12)
def raise_right_hand():
    # Command to move servo 11 to position 2000 and servo 12 to position 2000 over 1 second (1000 ms)
    send_command('#10P2000#11P1000#12P500T1000D800')  
    time.sleep(1)  # Wait for 1 second

# Function to return both servos (IDs 10 11 and 12) to the default position (1500)
def return_to_default():
    # Command to move servo 11 to position 1500 and servo 12 to position 1500 over 1 second (1000 ms)
    send_command('#10P1500#11P1950#12P1500T1000D800')  
    time.sleep(1)  # Wait for 1 second
def main():
    raise_right_hand()
    time.sleep(0.2)  # Keep the hand raised for 2 seconds
    return_to_default()

if __name__ == '__main__':
    main()

    # Close the serial connection
    ser.close()