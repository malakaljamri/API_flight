import socket
import threading
import api

flightsAPIManager: api.APIManager = None

class ClientHandler(threading.Thread):
    clientName: str = None
    def __init__(self, client_socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address


    def run(self):
        while True:
            try:
                if self.clientName == None:
                    self.client_socket.sendall("Enter your name: ".encode())# اشفر
                    data = self.client_socket.recv(1024).decode().strip() #فك 
                    if not data:
                        break
                    self.clientName = data
                    print(f"{self.clientName} Connected")
                    continue
                
                self.client_socket.sendall("1. Arrived flights\n2. Delayed flights\n3. All flights for a Country\n4. Details of Flight\nSelect an Option ('Quit' to disconnect): ".encode())
                
                data = self.client_socket.recv(1024).decode().strip() ####3333333
                if not data:
                    break

                if not data.isdigit(): ###
                    continue
                
                option = int(data)
                if option == 1:
                    print(f'{self.clientName} Requested all arrived flights')
                    self.client_socket.sendall(flightsAPIManager.all_arrived().encode())
                elif option == 2:
                    print(f'{self.clientName} Requested all delayed flights')
                    self.client_socket.sendall(flightsAPIManager.all_delayed().encode())
                elif option == 3:
                    self.client_socket.sendall('Enter Airport ICAO Code: '.encode())
                    code = self.client_socket.recv(1024).decode().strip() ####
                    if not code:
                        break

                    print(f'{self.clientName} Requested all flights from {code} Airport')
                    self.client_socket.sendall(flightsAPIManager.all_for(code).encode())
                elif option == 4:
                    self.client_socket.sendall('Enter Flight ICAO Code: '.encode())
                    code = self.client_socket.recv(1024).decode().strip()
                    if not code:
                        break

                    print(f'{self.clientName} Requested all info for Flight {code}')
                    self.client_socket.sendall(flightsAPIManager.info_for(code).encode())


            except Exception as e:
                print(f"Error: {e}")
                break

        if self.clientName != None:
            print(f"{self.clientName} just disconnected")
        self.client_socket.close()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                client_handler = ClientHandler(client_socket, address)
                client_handler.start()

        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            if self.server_socket:
                self.server_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'  # localhost
    PORT = 4999

    icao = input('Enter ICAO Code: ')
    flightsAPIManager = api.APIManager(icao)

    if len(flightsAPIManager.flights) == 0:
        print('An Error Happened while Fetching from the API')
        exit(1)

    server = Server(HOST, PORT)
    server.start()