import os
import socket
import tqdm
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '10.20.202.73'
server.bind((server_ip,9999))
server.listen()
client,addr = server.accept()
file_name = client.recv(4096).decode()
print(file_name)
time.sleep(1)
file_size = client.recv(4096).decode()
print(file_size)
time.sleep(1)
file = open(file_name,'wb')
file_bytes = b""
done  = False
progress = tqdm.tqdm(unit = "B", unit_scale = True , unit_divisor = 1000, total = int(file_size))
while not done:
    data = client.recv(1048576)
    if file_bytes[-5:] == b"<END>" :
        done = True
    else:
        file_bytes += data
    progress.update(len(data))
file.write(file_bytes)
file.close()
client.close()
server.close()
    
    
