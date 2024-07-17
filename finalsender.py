import os
import socket
import time
import tqdm

BUFFER_SIZE = 1048576

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_ip = input("Enter the IP address: ")
client.connect((client_ip, 9999))

nickname = input("Enter your nickname: ")
client.send(nickname.encode())
time.sleep(1)

done = False
while not done:
    file_n = input("Enter the file name you want to send (mention as it is in your folder) enter 'finished' if you want to exit sending file: ")
    if file_n != 'finished':
        if os.path.exists(file_n):
            file_size = os.path.getsize(file_n)
            client.send(f"recived_{file_n}".encode())
            time.sleep(1)
            client.send(str(file_size).encode())
            time.sleep(1)
            progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))
            with open(file_n, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    client.sendall(bytes_read)
                    progress.update(len(bytes_read))
            client.send(b"<END>")
            f.close()
        else:
            print("NO SUCH FILE EXISTS!")
    else:
        done = True

client.close()