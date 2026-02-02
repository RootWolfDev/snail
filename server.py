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
HOST = '0.0.0.0'
PORT = 5000
hostname=socket.gethostname()
locat=socket.gethostbyname(hostname)
print(locat)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

clients = []

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"{addr}: {message}")
            for client in clients:
                if client != conn:
                    client.sendall(f"HIM: {message}".encode())
        except Exception as e:
            print(e)
            break
    print(f"Connection closed: {addr}")
    clients.remove(conn)
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"SNAIL server listening on {HOST}:{PORT}")

    with context.wrap_socket(server, server_side=True) as tls_server:
        while True:
            conn, addr = tls_server.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()