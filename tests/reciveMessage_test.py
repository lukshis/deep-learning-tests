import socket

ip = "127.0.0.1"
port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))
sock.listen(5)

print("Starting to listen")

while True:
    print("Waiting for connection")
    connection, addr = sock.accept()
    print ("Accepted connection.")

    while True:
        message = connection.recv(64*64)
        if len(message) == 0:
            break
        print(message.decode())
        #connection.sendall(message.encode())
    
    connection.close()