import socket

ip = "192.168.1.102"
port = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))
message = "sending message"
while message != 'q':
    sock.send(bytes(message, 'utf-8'))
    data = sock.recv(64*64)
sock.close()