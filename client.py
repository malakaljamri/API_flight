import socket

SERVER_ADDRESS = ('127.0.0.1', 4999)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    # Check server down or up
    try:
        ss.connect(SERVER_ADDRESS)
    except ConnectionRefusedError:
        print('Server is not Online')
        exit(1)
    
    while True:
        response = ss.recv(1024).decode('utf-8')
        
        mode, msg = response.split('-', 1)
        if mode == "READ":
            i = input(msg)
            ss.send(i.encode('utf-8'))
        elif mode == "WRITE":
            print(msg)