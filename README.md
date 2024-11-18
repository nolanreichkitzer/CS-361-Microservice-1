# Weather Forecast Microservice

This microservice provides weather data, including current conditions, 5-day forecasts, and severe weather alerts. It communicates using **ZeroMQ** over TCP.  

---

## Communication Contract

### Overview
The microservice uses **JSON messages** sent over a ZeroMQ socket to handle requests and return responses.  
**Endpoint**: `tcp://<server_address>:5556`  
Replace `<server_address>` with the hostname or IP where the service is hosted. For me, it is 'localhost'.

### Supported Request Types
The following request types are supported:
1. `current_weather`: Fetches 12-hour weather data.
2. `5_day_forecast`: Fetches a 5-day weather forecast.
3. `severe_alert`: Fetches any severe weather alerts.

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

