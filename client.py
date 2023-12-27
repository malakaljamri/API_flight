import socket

SERVER_ADDRESS = ('127.0.0.1', 4999)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.connect(SERVER_ADDRESS)
    message = input("Enter your message: ")
    ss.send(message.encode('utf-8'))