import os
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_ip = '10.20.202.87'
client.connect((client_ip,9999))
file = open("unit.pdf","rb")
file_size = os.path.getsize("unit.pdf")
client.send("recived_unit.pdf".encode())
time.sleep(1)
client.send(str(file_size).encode())
time.sleep(1)
file_data = file.read()
client.sendall(file_data)
client.send(b"<END>")
file.close()
client.close()



