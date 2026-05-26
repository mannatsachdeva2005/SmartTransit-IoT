import json
import smtplib

from datetime import datetime

import paho.mqtt.client as mqtt

from pymongo import MongoClient

from geopy.distance import geodesic

from email.mime.text import MIMEText

# =====================================================
# MongoDB Connection
# =====================================================

mongo_client = MongoClient("mongodb://localhost:27017")

db = mongo_client["iot_backend"]

telemetry_collection = db["telemetry"]

alerts_collection = db["alerts"]

# =====================================================
# Email Configuration
# =====================================================

EMAIL_ADDRESS = "mannat.sachdeva2005@gmail.com"

EMAIL_PASSWORD = "sttx sktz yblc bzos"

RECEIVER_EMAIL = "mannat.sachdeva2005@gmail.com"

# =====================================================
# Geofence Settings
# =====================================================

GEOFENCE_CENTER = (28.6139, 77.2090)

GEOFENCE_RADIUS_KM = 2

# =====================================================
# Speed Settings
# =====================================================

MAX_SPEED = 80

# =====================================================
# MQTT Settings
# =====================================================

broker = "broker.hivemq.com"

port = 1883

topic = "smartbus/location"

# =====================================================
# Send Email Function
# =====================================================

def send_email_alert(subject, body):

    try:

        msg = MIMEText(body)

        msg["Subject"] = subject

        msg["From"] = EMAIL_ADDRESS

        msg["To"] = RECEIVER_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("Email alert sent")

    except Exception as e:

        print("Email Error:", e)

# =====================================================
# MQTT Connect Callback
# =====================================================

def on_connect(client, userdata, flags, rc):

    print("Connected to MQTT Broker")

    client.subscribe(topic)

# =====================================================
# MQTT Message Callback
# =====================================================

def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode()

        print("\nReceived:", payload)

        data = json.loads(payload)

        # =================================================
        # Add Timestamp
        # =================================================

        data["timestamp"] = datetime.utcnow()

        # =================================================
        # Store Telemetry
        # =================================================

        telemetry_collection.insert_one(data)

        print("Stored in MongoDB")

        # =================================================
        # Geofence Detection
        # =================================================

        bus_location = (
            data["latitude"],
            data["longitude"]
        )

        distance = geodesic(
            GEOFENCE_CENTER,
            bus_location
        ).km

        print(f"Distance from center: {distance:.2f} km")

        # =================================================
        # Geofence Alert
        # =================================================

        if distance > GEOFENCE_RADIUS_KM:

            geofence_alert = {

                "bus_id": data["bus_id"],

                "type": "Geofence Violation",

                "distance_km": round(distance, 2),

                "latitude": data["latitude"],

                "longitude": data["longitude"],

                "timestamp": datetime.utcnow()
            }

            alerts_collection.insert_one(
                geofence_alert
            )

            print("GEOFENCE ALERT")

            subject = f"Geofence Alert - {data['bus_id']}"

            body = f'''
ALERT!

Bus {data['bus_id']} has left the allowed zone.

Distance from center:
{distance:.2f} km
'''

            send_email_alert(subject, body)

        # =================================================
        # Overspeed Detection
        # =================================================

        if data["speed"] > MAX_SPEED:

            overspeed_alert = {

                "bus_id": data["bus_id"],

                "type": "Overspeed Alert",

                "speed": data["speed"],

                "timestamp": datetime.utcnow()
            }

            alerts_collection.insert_one(
                overspeed_alert
            )

            print("OVERSPEED ALERT")

            subject = f"Overspeed Alert - {data['bus_id']}"

            body = f'''
OVERSPEED ALERT!

Bus ID:
{data['bus_id']}

Current Speed:
{data['speed']} km/h

Maximum Allowed Speed:
{MAX_SPEED} km/h
'''

            send_email_alert(subject, body)

    except Exception as e:

        print("Error:", e)

# =====================================================
# MQTT Client Setup
# =====================================================

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(
    broker,
    port
)

print("MQTT Subscriber Running...")

client.loop_forever()