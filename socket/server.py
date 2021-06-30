import socket
import threading
# import time

# time.sleep(1)
# print("getting started with server")

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISSCONNECT_MSG ="!Disconnected"
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)

ADDR = (SERVER, PORT)
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv_sock.bind(ADDR)

def handle_cllient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected...")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISSCONNECT_MSG:
                connected = False
            print(f"[{addr}] {msg}")
    conn.close()

def start():
    serv_sock.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = serv_sock.accept()
        #creating thread
        thr = threading.Thread(target=handle_cllient, args=(conn, addr))
        thr.start()
        print("#"*20)
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()