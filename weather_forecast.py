# Name: Nolan Reichkitzer
# OSU Email: reichkin@oregonstate.edu
# Course: CS 361 - Software Engineering I
# Description: Microservice 1 - Weather Forecast
#
# 

import zmq
import requests
import time
from datetime import datetime

# Constants
NWS_API_URL = "https://api.weather.gov"
OPENCAGE_API_KEY = "aaeddb14e2294a78bd4bcff3755451f5"
TIMEOUT = 5

# ZeroMQ pipe setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


# Helper functions

def get_weather_data(endpoint):
    """Fetches data from the National Weather Service API"""
    try:
        response = requests.get(endpoint, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exception:
        print("Error fetching data from NWS API: " + str(exception))
        return {"error": "Unable to fetch weather data"}


def get_coordinates_from_zipcode(zipcode):
    """Convert ZIP code to latitude and longitude using OpenCage Geocoding API"""
    
    url = "https://api.opencagedata.com/geocode/v1/json?countrycode=us&q=" + zipcode + "&key=" + OPENCAGE_API_KEY
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            return None, None
    except requests.RequestException as exception:
        print("Error fetching coordinates: " + str(exception))
        return None, None
    
def parse_datetime(datetime_str):
    """Parses the input datetime string into a more readable format"""

    # Parse the input string into datetime object
    datetime_object = datetime.fromisoformat(datetime_str)

    # Format the output
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S")


def get_current_weather(zipcode):
    """Gets current 12-hour weather data for a given US zipcode"""

    # Fetch the latitude and longitute of the input zipcode
    latitude, longitude = get_coordinates_from_zipcode(zipcode)

    if latitude is None or longitude is None:
        return {"error": "Invalid zipcode or error fetching coordinates"}

    # Fetch the current weather data for the location
    endpoint = NWS_API_URL + "/points/" + str(latitude) + "," + str(longitude)
    coordinate_data = get_weather_data(endpoint)

    # Fetch the hourly forecast data
    if coordinate_data['properties']:
        endpoint = coordinate_data['properties']['forecastHourly']
        forecast_data = get_weather_data(endpoint)
        hourly_forecast_list = forecast_data['properties']['periods'][:12]

        # Remove unnecessary elements from the ouput
        for element in hourly_forecast_list:
            del element['name']
            del element['isDaytime']
            del element['temperatureTrend']
            del element['icon']
            del element['detailedForecast']
            element['startTime'] = parse_datetime(element['startTime'])
            element['endTime'] = parse_datetime(element['endTime'])

        return hourly_forecast_list


def get_5_day_forecast(zipcode):
    """Gets a 5-day weather forecast for a given US zipcode"""

    # Fetch the latitude and longitute of the input zipcode
    latitude, longitude = get_coordinates_from_zipcode(zipcode)

    if latitude is None or longitude is None:
        return {"error": "Invalid zipcode or error fetching coordinates"}

    # Fetch the current weather data for the location
    endpoint = NWS_API_URL + "/points/" + str(latitude) + "," + str(longitude)
    coordinate_data = get_weather_data(endpoint)

    # Fetch the 5-day forecast data
    if coordinate_data['properties']:
        endpoint = coordinate_data['properties']['forecast']
        forecast_data = get_weather_data(endpoint)
        forecast_list = forecast_data['properties']['periods'][:12]

        # Remove unnecessary elements from the ouput
        for element in forecast_list:
            del element['isDaytime']
            del element['temperatureTrend']
            del element['icon']
            element['startTime'] = parse_datetime(element['startTime'])
            element['endTime'] = parse_datetime(element['endTime'])

        return forecast_list


def get_severe_weather_alerts(zipcode):
    """Checks for severe weather alerts for a given US zipcode"""
    
    # Fetch the latitude and longitute of the input zipcode
    latitude, longitude = get_coordinates_from_zipcode(zipcode)

    if latitude is None or longitude is None:
        return {"error": "Invalid zipcode or error fetching coordinates"}

    # Fetch the current weather data for the location
    endpoint = NWS_API_URL + "/points/" + str(latitude) + "," + str(longitude)
    coordinate_data = get_weather_data(endpoint)

    # Fetch the active alerts for the location
    if coordinate_data['properties']:
        forecast_zone = coordinate_data['properties']['forecastZone'].split("/")[-1]
        endpoint = NWS_API_URL + "/alerts/active/zone/" + forecast_zone
        alert_data = get_weather_data(endpoint)
        alert_list = alert_data['features']
        formatted_list = []

        # Create a more readable output
        for index, element in enumerate(alert_list):
            new_dict = {
                'number': index,
                'effective': parse_datetime(element['properties']['effective']),
                'expires': parse_datetime(element['properties']['expires']),
                'severity': element['properties']['severity'],
                'headline': element['properties']['headline'],
                'description': element['properties']['description'],
                'instruction': element['properties']['instruction']
            }
            formatted_list.append(new_dict)

        return formatted_list

# Main server loop

print("Weather forecast microservice listening for requests...")
while True:
    
    message = socket.recv_json()
    request_type = message["type"]
    zipcode = message["zipcode"]
    response = {}

    start_time = time.time()

    if request_type == "current_weather":
        # Check current weather conditions
        response = get_current_weather(zipcode)
    elif request_type == "5_day_forecast":
        # Get 5-day weather forecast
        response = get_5_day_forecast(zipcode)
    elif request_type == "severe_alert":
        # Check for severe weather alerts
        response = get_severe_weather_alerts(zipcode)
    else:
        response = {"error": "Invalid request type"}

    # Check for timeout
    time_diff = time.time() - start_time
    if time_diff > TIMEOUT:
        response = {"error": "Request timed out"}

    # Send the response back to the client
    socket.send_json(response)
