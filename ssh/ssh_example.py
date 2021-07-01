# Example from the documentation file
import os
import socket
from ssh2.session import Session

host = 'localhost'
user = 'enter ur user name'
password = 'enter ur password'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, 22))

session = Session()
session.handshake(sock)
session.userauth_password(user, password)

channel = session.open_session()
channel.execute('echo me; exit 2')
size, data = channel.read()
while size > 0:
    print(data)
    size, data = channel.read()
channel.close()
print("Exit status: %s" % channel.get_exit_status())