# Weather Forecast Microservice

This microservice provides weather data, including current conditions, 5-day forecasts, and severe weather alerts. It communicates using **ZeroMQ** over TCP.  

---

## Communication Contract

### Overview
The microservice uses **JSON messages** sent over a ZeroMQ socket to handle requests and return responses.  
**Endpoint**: `tcp://<server_address>:5555`  
Replace `<server_address>` with the hostname or IP where the service is hosted.

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
