import socket, threading
from api import APIManager, FlightData
from typing import List, Tuple

SERVER_ADDRESS = ('127.0.0.1', 4999)

class Client:
    name: str # the client name
    client_socket: socket.socket
    client_address: Tuple

    def __init__(self, sock: socket.socket, addr) -> None:
        # self is same as this in java
        self.name = "malak"
        self.client_address = addr
        self.client_socket = sock

    def read(self) -> str:
        response = self.client_socket.recv(1024)
        return response.decode('utf-8')

    def write(self, msg: str) -> None:
        self.client_socket.send(msg.encode('utf-8'))

    def get_name(self) -> str:
        self.write('READ-Enter Your Name: ')
        n = self.read()
        self.name = n
        return n
        


class FlightsServer:
    flights: List[FlightData]
    server_socket: socket.socket

    def __init__(self, flights: List[FlightData]) -> None:
        self.flights = flights
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:
            ss.bind(SERVER_ADDRESS)
            ss.listen(10) # max conns = 10
            self.server_socket = ss

            self.listen()
    
    def listen(self) -> None:
        print(f'Server listening on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
        while True:
            client_socket, client_address = self.server_socket.accept()
            c = Client(client_socket, client_address)

            # Put connection on Separate thread
            client_thread = threading.Thread(target=self.handle_client, args=(c,))
            # Start Thread
            client_thread.start()


    # This will handle the client connect until it disconnects
    @classmethod
    def handle_client(self, c: Client) -> None:
        data = c.get_name()
        print(f'Recieved "{data}" from {c.client_address}')


icao = input('Enter ICAO Code: ')

f = APIManager.fetchFlights(icao)

if f == None:
    print("An Error Happened While Fetching")
    exit(1)

server = FlightsServer(f)
