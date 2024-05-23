import serial
import time

# Open a serial connection to the servo controller
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Function to send a command to the servo controller
def send_command(command):
    ser.write((command + '\r\n').encode())  # Add '\r\n' for CRLF
    time.sleep(0.1)  # Short delay to ensure command is sent
# Function to balance the hands    
def balance_the_hands():
    send_command('#6P1500#7P1100#8P1500#10P1500#11P1950#12P1500T1000D800')  # Adjust positions for balancing the hands
    time.sleep(1)  # Wait for 1 second
 
# Function to balance the left leg
def balance_left_leg():
    send_command('#1P1400#2P1300#3P900#4P1300#5P1350T1000D800')  # Adjust positions for balancing the left leg
    time.sleep(1)  # Wait for 1 second

# Function to balance the right leg
def balance_right_leg():
    send_command('#17P1850#16P1550#15P1300#14P900#13P1450T1000D800')  # Adjust positions for balancing the right leg
    time.sleep(1)  # Wait for 1 second
def main():
    balance_the_hands()
    balance_left_leg()
    balance_right_leg()
if __name__ == '__main__':
    main()
   
    # Close the serial connection
    ser.close()