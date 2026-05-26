import json
import random
import time

import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"

port = 1883

topic = "smartbus/location"

client = mqtt.Client()

client.connect(broker, port)

# =====================================================
# Bus Definitions
# =====================================================

buses = [

    {
        "bus_id": "BUS101",
        "latitude": 28.6139,
        "longitude": 77.2090
    },

    {
        "bus_id": "BUS102",
        "latitude": 28.6239,
        "longitude": 77.2190
    },

    {
        "bus_id": "BUS103",
        "latitude": 28.6339,
        "longitude": 77.2290
    }
]

# =====================================================
# Live Simulation
# =====================================================

while True:

    for bus in buses:

        # Small movement
        bus["latitude"] += random.uniform(-0.001, 0.001)

        bus["longitude"] += random.uniform(-0.001, 0.001)

        data = {

            "bus_id": bus["bus_id"],

            "latitude": round(bus["latitude"], 6),

            "longitude": round(bus["longitude"], 6),

            "speed": random.randint(40, 100),

            "passengers": random.randint(5, 40),

            "status": "active"
        }

        payload = json.dumps(data)

        client.publish(topic, payload)

        print("Published:", payload)

    time.sleep(5)