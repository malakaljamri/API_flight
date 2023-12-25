import  requests, json

API_URL = 'http://api.aviationstack.com/v1/flights'

ACCESS_KEY = 'bc3afa47496ff14131de64609f8a5d07'


ICAO = 'OBBI' # Bahrain airpot code


params = {
    'access_key': ACCESS_KEY,
    'arr_icao': ICAO
}

flights = requests.get(API_URL, params)
# print(flights.text)

flights_json = flights.json()

with open('flights.json', 'w') as file:
    file.write(json.dumps(flights_json))