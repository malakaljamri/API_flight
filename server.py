from api import APIManager

icao = input('Enter ICAO Code: ')

flights = APIManager.fetchFlights(icao)

if flights == None:
    print("An Error Happened While Fetching")
    exit(1)

print(flights)