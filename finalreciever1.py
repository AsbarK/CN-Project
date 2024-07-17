import os
import socket
import tqdm
import time
import threading
import queue

def handle_client(client, addr, clients, send_queue):
    nickname = client.recv(4096).decode()
    time.sleep(1)
    clients[nickname] = client
    print(f"{nickname} joined the server")
    file_name = client.recv(4096).decode()
    print(f"{nickname} is sending {file_name}")
    time.sleep(1)
    file_size = client.recv(4096).decode()
    print(f"{file_name} size: {file_size}")
    time.sleep(1)
    file = open(file_name,'wb')
    file_bytes = b""
    done  = False
    progress = tqdm.tqdm(unit = "B", unit_scale = True , unit_divisor = 1000, total = int(file_size))
    
    # Try to add the sender to the queue, if it's already in the queue, wait
    while nickname in send_queue:
        time.sleep(1)
    send_queue.append(nickname)
    
    while not done:
        data = client.recv(1048576)
        if file_bytes[-5:] == b"<END>" :
            done = True
        else:
            file_bytes += data
        progress.update(len(data))
    file.write(file_bytes)
    file.close()
    print(f"{file_name} received from {nickname}")
    
    # Remove the sender from the queue
    send_queue.remove(nickname)
    
    for client_nickname, client_socket in clients.items():
        if client_nickname != nickname:
            client_socket.send(f"{nickname} sent {file_name}".encode())
            client_socket.send(file_name.encode())
            time.sleep(1)
            client_socket.send(file_size.encode())
            time.sleep(1)
            client_socket.sendall(file_bytes)
            client_socket.send(b"<END>")
    client.close()
    del clients[nickname]
    print(f"{nickname} left the server")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_nsme = socket.gethostname()
server_ip = socket.gethostbyname(socket.gethostname())
print(server_ip)
server.bind((server_ip,9999))
server.listen()
clients = {}
send_queue = queue.Queue()

while True:
    client,addr = server.accept()
    print(f"New connection from {addr}")
    threading.Thread(target=handle_client, args=(client, addr, clients, send_queue)).start()
