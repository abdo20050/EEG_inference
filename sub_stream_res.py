import socket
import pickle
import numpy as np
# import struct
import atexit
import zlib
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
atexit.register(sock.close)
# server_address = ('localhost', 12345)  # Change to your server IP and port

# # Send data
# message = b'This is the message. It will be sent in UDP.'
# sock.sendto(message, server_address)
# sock.close()
sock.bind(('0.0.0.0', 12345))
# Receive response
i = 0
print("wait headset data!")
sock.listen(2)
conn, addr = sock.accept()
print("goooo!")
last_seq = 0
def main():
    global conn, last_seq
    data_array = np.empty((0,14))
    # print('waiting to receive')
    # data, server = sock.recvfrom(pow(2,30))
    while(data_array.shape[0] < 1125):
        
        message = conn.recv(pow(2,20))
        try:
            np_data, sequance_num = tuple(pickle.loads(zlib.decompress(message)))
            
            if sequance_num <= last_seq:
                # continue
                pass

            received_arr = np.array(np_data)
            data_array = np.append(data_array, received_arr, axis=0)
            print('received {!r}'.format(int(sequance_num)))
        except Exception as e:
            # print(e)d
            pass
    # print(data_array)
    last_seq = int(sequance_num)+1
    return data_array
        # data_array = np.empty((0,14), float)
if __name__ == "__main__":
    while 1:
        main()
    
