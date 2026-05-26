
# SmartTransit IoT

SmartTransit IoT is a real-time smart bus and fleet monitoring backend system built using FastAPI, MQTT, MongoDB, and WebSockets.

The project simulates multiple IoT-enabled buses sending live telemetry data such as GPS location, speed, fuel level, engine status, and temperature through MQTT. The backend processes and stores telemetry data in MongoDB while providing REST APIs and real-time dashboard updates.

The system includes:
- Live GPS tracking
- MQTT-based telemetry ingestion
- MongoDB storage
- Real-time APIs
- WebSocket live updates
- Geofencing and alert system
- Multi-device fleet monitoring
- Real-time dashboard visualization

This project demonstrates practical IoT backend engineering concepts used in real-world fleet management and smart transportation systems.
## Features

- Real-time GPS tracking
- MQTT communication
- Multiple vehicle simulation
- MongoDB telemetry storage
- REST APIs using FastAPI
- WebSocket live updates
- Live dashboard visualization
- Overspeed alerts
- Geofencing support
- Device telemetry analytics
- Fleet monitoring system
- IoT Devices → MQTT Broker → FastAPI Backend → MongoDB → REST APIs/WebSockets → Live Dashboard
