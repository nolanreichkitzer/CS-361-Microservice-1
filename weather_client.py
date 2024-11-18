# Name: Nolan Reichkitzer
# OSU Email: reichkin@oregonstate.edu
# Course: CS 361 - Software Engineering I
# Description: Microservice 1 - Client
#
# 

import zmq


def send_request(request_type, zipcode):
    """Sends a request to the microservice and receives a response"""
    
    request = {
        "type": request_type,
        "zipcode": zipcode
    }
    
    try:
        # Send the request
        print("Sending request: " + str(request))
        socket.send_json(request)
        
        # Wait for the response and print
        response = socket.recv_json()
        print(response)

    except Exception as exception:
        print("Error communicating with microservice: " + exception)


if __name__ == "__main__":

    # ZeroMQ pipe setup
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    # Print request options
    print("Weather Client")
    print("Options:")
    print("1. Current Weather")
    print("2. 5-Day Forecast")
    print("3. Severe Weather Alerts")
    print("4. Exit")
        
    while True:
        # Get user input
        option = input("Choose an option: ")
        if option == "4":
            print("Exiting client")
            break
            
        zipcode = input("Enter location (US zipcode): ")
            
        if option == "1":
            send_request("current_weather", zipcode)
        elif option == "2":
            send_request("5_day_forecast", zipcode)
        elif option == "3":
            send_request("severe_alert", zipcode)
        else:
            print("Invalid option. Please try again.")