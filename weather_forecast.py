# Name: Nolan Reichkitzer
# OSU Email: reichkin@oregonstate.edu
# Course: CS 361 - Software Engineering I
# Description: Microservice 1 - Weather Forecast
#
# 

import zmq
import json
import time

# Constants
NWS_API_URL = "https://api.weather.gov"

# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")  # This will listen on port 5555

# Helper functions

def get_current_weather(location: str):
    """Gets current weather data for a given location."""
    pass


def get_5_day_forecast(location: str):
    """Gets a 5-day weather forecast for a given location."""
    pass


def get_severe_weather_alerts(location: str):
    """Checks for severe weather alerts for a given location."""
    pass

# Main server loop

