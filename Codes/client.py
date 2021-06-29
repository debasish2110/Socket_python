import socket

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISSCONNECT_MSG ="!Disconnected"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(ADDR)

def send_signal(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #b' ' represents byte representatin
    client_sock.send(send_length)
    client_sock.send(message)

send_signal("Socket programming....")
send_signal("sending message 1")
send_signal("sending message 2")
send_signal(DISSCONNECT_MSG)