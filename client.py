import socket

SERVER_ADDRESS = ('127.0.0.1', 4999)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.connect(SERVER_ADDRESS)
    response = ss.recv(1024).decode('utf-8')
    
    mode, msg = response.split('-', 1)
    if mode == "READ":
        i = input(msg)
        ss.send(i.encode('utf-8'))
    elif mode == "WRITE":
        print(msg)