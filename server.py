import socket, threading
from api import APIManager, FlightData
from typing import List, Tuple

SERVER_ADDRESS = ('127.0.0.1', 4999)

class Client:
    name: str # the client name
    client_socket: socket.socket
    client_address: Tuple
    thread: threading.Thread

    def __init__(self, sock: socket.socket, addr) -> None:
        # self is same as this in java
        self.client_address = addr
        self.client_socket = sock

    def read(self) -> str:
        response = self.client_socket.recv(1024)
        return response.decode('utf-8')

    def write(self, msg: str) -> None:
        try:
            self.client_socket.send(msg.encode('utf-8'))
        except:
            # Client Disconnected
            print(f'{self.name} Disconnected')
            raise ConnectionError

    def get_name(self) -> str:
        self.write('READ-Enter Your Name: ')
        n = self.read()
        self.name = n
        return self.name
    
    def write_options(self) -> None:
        msg = 'READ-'
        msg += '1. Arrived flights\n2. Delayed flights\n3. All flights for a Country\n4. Details of Flight\n'
        msg += 'Select an Option(1-4): '

        self.write(msg)
        resp = self.read()

        if not resp.isdigit():
            self.write('WRITE-Invalid Option')
            self.write_options()
            return

        option = int(resp)
        if option < 1 or option > 4:
            self.write('WRITE-Invalid Option')
            self.write_options()
            return

        print(f'CorrecT! Selected {option}')
        


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
            c.thread = client_thread
            # Start Thread
            c.thread.start()


    def logClient(self, c: Client) -> None:
        print(f'{c.name} Connected')

    # This will handle the client connect until it disconnects
    def handle_client(self, c: Client) -> None:
        c.get_name()
        self.logClient(c)

        try:
            while True:
                c.write_options()
        except:
            c.thread.join()

    


icao = input('Enter ICAO Code: ')

f = APIManager.fetchFlights(icao)

if f == None:
    print("An Error Happened While Fetching")
    exit(1)

server = FlightsServer(f)
