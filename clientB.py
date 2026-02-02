from rich import print
import socket
import threading
import ssl
print(r'''
  _________             .__.__   
 /   _____/ ____ _____  |__|  |  
 \_____  \ /    \\__  \ |  |  |  
 /        \   |  \/ __ \|  |  |__
/_______  /___|  (____  /__|____/
        \/     \/     \/         
''')

HOST = '192.168.1.205'
PORT = 12345

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  

def receive_messages(ssock):
    while True:
        try:
            data = ssock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print("Connected to SNAIL server via ")

        threading.Thread(target=receive_messages, args=(ssock,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            ssock.sendall(msg.encode())