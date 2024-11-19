# Weather Forecast Microservice

This microservice provides weather data, including current conditions, 5-day forecasts, and severe weather alerts. It communicates using **ZeroMQ** over TCP.  

---

## Communication Contract

### Overview
The microservice uses **JSON messages** sent over a ZeroMQ socket to handle requests and return responses.  
**Endpoint**: `tcp://<server_address>:5556`  
Replace `<server_address>` with the hostname or IP where the service is hosted. For me, it is "localhost".

### Supported Request Types
The following request types are supported:
1. `current_weather`: Fetches 12-hour weather data.
2. `5_day_forecast`: Fetches a 5-day weather forecast.
3. `severe_alert`: Fetches any severe weather alerts.

### Dependencies
Ensure your environment has the following installed:
- Python 3.x
- pyzmq
- requests

The following code can be run in the terminal to install pyzmq and requests.
``` bash
pip install pyzmq requests
```

### Accessing the Microservice
To access the microservice:
- Clone this repository
- Open a terminal session and navigate to the repository directory
- Run the microservice locally using the command:
  
```bash
py weather_forecast.py
```

###
---

## How to Request Data

### Protocol
- Use ZeroMQ with a **REQ/REP** socket type.
- Send a JSON message containing the request details.
- Wait for the JSON response.

### JSON Request Format
Each request must include:
- `type` (string): The type of data you are requesting. Options: `current_weather`, `5_day_forecast`, `severe_alert`.
- `zipcode` (string): A valid U.S. ZIP code.

#### Example Request
```json
{
  "type": "current_weather",
  "zipcode": "10001"
}
```

#### Example Code
```python
import zmq

# Set up ZeroMQ client
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://<server_address>:5556")  # Replace with actual address

# Create the request
request = {
    "type": "current_weather",
    "zipcode": "10001"
}

# Send the request
socket.send_json(request)

# Wait for the response
response = socket.recv_json()
print("Response:", response)
```
*Note: This is example code. You will likely need to adjust it for your needs.


## How to Receive Data

### JSON Response Format
The response is always a JSON object.
- For current_weather: A list of up to 12 hourly forecasts.
- For 5_day_forecast: A list of daily forecasts.
- For severe_alert: A list of active severe weather alerts.

#### Example Response for current_weather
``` json
[
  {
    "number": "1",
    "startTime": "2024-11-18 21:00:00",
    "endTime": "2024-11-18 22:00:00",
    "temperature": "75",
    "temperatureUnit": "F",
    "probabilityOfPrecipitation": {"unitCode": "wmoUnit:percent", "value": "1"},
    "dewpoint": {"unitCode": "wmoUnit:degC", "value": "17.77777777777778"},
    "relativeHumidity": {"unitCode": "wmoUnit:percent", "value": "69"},
    "windSpeed": "6 mph",
    "windDirection": "E",
    "shortForecast": "Mostly Cloudy"
  },
  {
    "number": "2",
    "startTime": "2024-11-18 22:00:00",
    "endTime": "2024-11-18 23:00:00",
    "temperature": "75",
    "temperatureUnit": "F",
    "probabilityOfPrecipitation": {"unitCode": "wmoUnit:percent", "value": "2"},
    "dewpoint": {"unitCode": "wmoUnit:degC", "value": "17.77777777777778"},
    "relativeHumidity": {"unitCode": "wmoUnit:percent", "value": "69"},
    "windSpeed": "6 mph",
    "windDirection": "E",
    "shortForecast": "Mostly Cloudy"
  }
*continued
]
```

#### Example Response for 5_day_forecast
``` json
[
  {
    "number": "1",
    "name": "Tonight",
    "startTime": "2024-11-18 21:00:00",
    "endTime": "2024-11-19 06:00:00",
    "temperature": "72",
    "temperatureUnit": "F",
    "probabilityOfPrecipitation": {"unitCode": "wmoUnit:percent", "value": "None"},
    "windSpeed": "6 mph",
    "windDirection": "SE",
    "shortForecast": "Partly Cloudy",
    "detailedForecast": "Partly cloudy, with a low around 72. Southeast wind around 6 mph."
  },
  {
    "number": "2",
    "name": "Tuesday",
    "startTime": "2024-11-19 06:00:00",
    "endTime": "2024-11-19 18:00:00",
    "temperature": "81",
    "temperatureUnit": "F",
    "probabilityOfPrecipitation": {"unitCode": "wmoUnit:percent", "value": "None"},
    "windSpeed": "5 to 10 mph",
    "windDirection": "SE",
    "shortForecast": "Mostly Sunny",
    "detailedForecast": "Mostly sunny, with a high near 81. Southeast wind 5 to 10 mph."
  }
*continued
]

```

#### Example Response for severe_alert
``` json
[
  {
    "number": 0,
    "effective": "2024-11-18 14:00:00",
    "expires": "2024-11-18 18:00:00",
    "severity": "Severe",
    "headline": "Severe Thunderstorm Warning",
    "description": "A severe thunderstorm has been detected...",
    "instruction": "Seek shelter indoors immediately."
  }
*continued
]

```


### UML - Sequence Diagram

This sequence diagram describes the interactions between the programs.

![image](https://github.com/user-attachments/assets/ba994623-96f8-4c9e-b35e-ce6dc168b6c8)
