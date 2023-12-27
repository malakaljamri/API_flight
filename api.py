import  requests, json, logging
from dataclasses import dataclass, field
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
    @staticmethod
    def fetchFlights(arr_icao: str) -> None|List[FlightData]:
        print(f'Fetching flights for {arr_icao}')
        params = {
            'access_key': ACCESS_KEY,
            'arr_icao': arr_icao,
            'limit': 100
        }
        flightsRaw = requests.get(API_URL, params)
        if flightsRaw.status_code != 200:
            return None
        
        fligtsJson = flightsRaw.json()
        with open('GB11.json', 'w') as file:
            file.write(json.dumps(fligtsJson['data']))  

        flights_arr: List[FlightData] = []
        for flight in fligtsJson['data']:
            flights_arr.append(FlightData(**flight))
        print('Fetched Flights')
        return flights_arr