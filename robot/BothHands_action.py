import serial
import time

# Open a serial connection to the servo controller
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Function to send a command to the servo controller
def send_command(command):
    ser.write((command + '\r\n').encode())  # Add '\r\n' for CRLF
    time.sleep(0.1)  # Short delay to ensure command is sent
    
def raise_both_hands():
    # Command to move servo 11 to position 2000 and servo 12 to position 2000 over 1 second (1000 ms)
    send_command('#6P2300#7P2300#8P700#10P2000#11P1000#12P500#9P2000T1000D800')  
    time.sleep(1)  # Wait for 1 second
    
def balance_the_hands():
    send_command('#6P1500#7P1100#8P1500#10P1500#11P1950#12P1500#9P1400T1000D800')  # Adjust positions for balancing the hands
    time.sleep(1)  # Wait for 1 second
def main():
    raise_both_hands()
    time.sleep(0.2)  # Keep the hand raised for 2 seconds
    balance_the_hands()

if __name__ == '__main__':
    main()
    # Close the serial connection
    ser.close()    