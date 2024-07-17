import socket
import time

ip_address = '127.0.0.1'
port_range = range(0,65536)
numofport = 0
typeofport = []

for port in port_range:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip_address, port))
    # time.sleep(2)
    if result == 0:
        numofport = numofport + 1
        typeofport.append(port)
    else:
        # print(f"close{port}")
        continue
    sock.close()
print(f"Total number of open ports: {numofport}")
if numofport > 0:
    print("Open ports:")
    for i in range(0,numofport):
        print(typeofport[i])
else:
    print("No open ports found.")
