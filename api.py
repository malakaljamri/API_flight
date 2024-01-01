import  requests, json
from dataclasses import dataclass
from typing import Optional, List

API_URL = 'http://api.aviationstack.com/v1/flights'

ACCESS_KEY = 'bc3afa47496ff14131de64609f8a5d07'

@dataclass
class Departure:
    airport: str
    timezone: str
    iata: str
    icao: str
    terminal: Optional[None]
    gate: Optional[None]
    delay: Optional[None]
    scheduled: str
    estimated: str
    actual: Optional[None]
    estimated_runway: Optional[None]
    actual_runway: Optional[None]

@dataclass
class Arrival:
    airport: str
    timezone: str
    iata: str
    icao: str
    terminal: Optional[None]
    gate: Optional[None]
    baggage: Optional[None]
    delay: Optional[None]
    scheduled: str
    estimated: str
    actual: Optional[None]
    estimated_runway: Optional[None]
    actual_runway: Optional[None]

@dataclass
class Airline:
    name: str
    iata: str
    icao: str

@dataclass
class Flight:
    number: str
    iata: str
    icao: str
    codeshared: Optional[None]

@dataclass
class FlightData:
    flight_date: str
    flight_status: str
    departure: Departure
    arrival: Arrival
    airline: Airline
    flight: Flight
    aircraft: Optional[None] = None
    live: Optional[None] = None



class APIManager:
    flights: List[FlightData] = []

    def __init__(self, arr_icao: str) -> None:
        print(f'Fetching flights for {arr_icao}')
        params = {
            'access_key': ACCESS_KEY,
            'arr_icao': arr_icao,
            'limit': 100
        }
        flightsRaw = requests.get(API_URL, params)
        if flightsRaw.status_code != 200:
            print(flightsRaw.text)
            return None
        
        # # to load locally
        # fligtsJson = ''
        # with open('GB11.json', 'r') as file:
        #     fligtsJson = json.load(file)

        fligtsJson = flightsRaw.json()
        with open('GB11.json', 'w') as file:
            file.write(json.dumps(fligtsJson['data']))  
        for flight in fligtsJson['data']:
        # for flight in fligtsJson:
            self.flights.append(FlightData(**flight))
        print('Fetched Flights')
        
    def all_arrived(self) -> str:
        resp = ''
        for flight in self.flights:
            if flight.flight_status == 'landed':
                resp += f'IATA Code: {flight.flight["iata"]}\nDeparture AirPort: {flight.departure["airport"]}\n'
                resp += f'Arrival Time: {flight.arrival["actual"]}\n Arrival Terminal: {flight.arrival["terminal"]}\n'
                resp += f'Arrival Gate: {flight.arrival["gate"]}'
                resp += '\n\n'
        return resp
    def all_delayed(self) -> str:
        resp = ''
        for flight in self.flights:
            if flight.flight_status == 'landed' and flight.departure.get('delay') != None and flight.departure['delay'] > 0:
                resp += f'IATA Code: {flight.flight["iata"]}\nDeparture AirPort: {flight.departure["airport"]}\n'
                resp += f'Departure Time: {flight.departure["scheduled"]}\nEstimated Arrival Time : {flight.arrival["estimated"]}\n'
                resp += f'Arrival Terminal: {flight.arrival["terminal"]}\nDelay: {flight.departure["delay"]} minutes\nArrival Gate: {flight.arrival["gate"]}'
                resp += '\n\n'
        return resp

    def all_for(self, departure_icao: str) -> str:
        resp = ''
        for flight in self.flights:
            if flight.departure['icao'] == departure_icao:
                resp += f'IATA Code: {flight.flight["iata"]}\nDeparture AirPort: {flight.departure["airport"]}\n'
                resp += f'Departure Time: {flight.departure["scheduled"]}\nEstimated Arrival Time : {flight.arrival["estimated"]}\n'
                resp += f'Departure Gate: {flight.departure["gate"]}\nArrival Gate: {flight.arrival["delay"]}\nStatus: {flight.flight_status}'
                resp += '\n\n'
        return resp
    
    def info_for(self, flight_icao: str) -> str:
        resp = ''
        for flight in self.flights:
            if flight.flight['icao'] == flight_icao:
                resp += f'IATA Code: {flight.flight["iata"]}\nDeparture AirPort: {flight.departure["airport"]}\n'
                resp += f'Departure Gate: {flight.departure["gate"]}\nDeparture Terminal: {flight.departure["terminal"]}\n'
                resp += f'Arrival Airport: {flight.arrival["airport"]}\nArrival Gate: {flight.arrival["gate"]}\nArrival Terminal: {flight.arrival["terminal"]}\n'
                resp += f'Status: {flight.flight_status}\nScheduled Departure Time: {flight.departure["scheduled"]}\nScheduled Arrial Time: {flight.arrival["scheduled"]}'
                resp += '\n\n'
        return resp