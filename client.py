import socket

class TCPClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print(f"Connected to {self.server_address}:{self.server_port}")
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            exit()

    def send_receive_data(self):
        try:
            while True:
                # Receive data from the server
                data = self.client_socket.recv(1024*10*5)

                # Ask user for input
                user_input = input(data.decode())

                # Send user input back to the server
                self.client_socket.sendall(user_input.encode())

                if user_input.lower() == 'Quit':
                    break
        except KeyboardInterrupt:
            print('\nConnection Closed by User')
        except Exception as e:
            print(f"Error sending/receiving data: {e}")
        finally:
            # Close the socket
            self.client_socket.close()

if __name__ == "__main__":
    # Set the server address and port
    server_address = "localhost"
    server_port = 4999

    # Create an instance of the TCPClient
    client = TCPClient(server_address, server_port)

    # Connect to the server
    client.connect_to_server() 

    # Send and receive data in an infinite loop
    client.send_receive_data()
