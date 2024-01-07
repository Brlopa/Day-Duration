import json
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

data_url = "https://api.sunrisesunset.io/json?"
cities_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records?select=name%2C%20coordinates&limit=100"
cities_response = requests.get(cities_url)
cities_names = [name["name"] for name in cities_response.json()["results"]]
cities_lat = [coordinates["coordinates"]["lat"] for coordinates in cities_response.json()["results"]]
cities_lon = [coordinates["coordinates"]["lon"] for coordinates in cities_response.json()["results"]]
dayDurationList=[] 

def dayDuration(lat,lng):
    daySum = timedelta()
    parameters = {
        "lat": lat ,
        "lng" : lng,
        "date_start": "2023-01-01",
        "date_end": "2023-12-31"
    }
    data_response = requests.get(data_url,params=parameters)
    sunrise_data = [sunrise["sunrise"] for sunrise in data_response.json()["results"]]
    sunset_data = [sunrise["sunset"] for sunrise in data_response.json()["results"]]
    
    sunrise_data_formatted = list(filter(lambda item: item is not None, sunrise_data))
    sunrset_data_formatted = list(filter(lambda item: item is not None, sunset_data))

    for sunrise, sunset in zip(sunrise_data_formatted,sunrset_data_formatted):    
        sunset_formatted = datetime.strptime(sunset, "%I:%M:%S %p")
        sunrise_formatted = datetime.strptime(sunrise, "%I:%M:%S %p")
        day = sunset_formatted-sunrise_formatted
        daySum += day

    return(daySum.total_seconds()/(60*60))
 
for name, lat, lon in zip(cities_names,cities_lat,cities_lon):
    #print(name)
    dayDurationList.append(dayDuration(lat,lon))

print(dayDurationList)

plt.plot(cities_lat,dayDurationList)
plt.show()