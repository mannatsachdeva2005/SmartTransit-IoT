from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017")

db = client["iot_backend"]
collection = db["telemetry"]


def convert_id(data):
    data["_id"] = str(data["_id"])
    return data


@app.get("/")
def home():
    return {"message": "Smart Bus Tracking Backend Running"}


@app.get("/locations")
def get_locations():

    pipeline = [
        {
            "$sort": {"timestamp": -1}
        },
        {
            "$group": {
                "_id": "$bus_id",
                "latest": {"$first": "$$ROOT"}
            }
        }
    ]

    data = list(collection.aggregate(pipeline))

    result = []

    for item in data:
        latest = item["latest"]
        latest["_id"] = str(latest["_id"])
        result.append(latest)

    return result
@app.get("/alerts")
def get_alerts():

    alerts_collection = db["alerts"]

    alerts = list(
        alerts_collection.find().sort(
            "timestamp",
            -1
        ).limit(20)
    )

    for alert in alerts:

        alert["_id"] = str(alert["_id"])

    return alerts
@app.get("/bus/{bus_id}")
def get_bus(bus_id: str):
    data = list(collection.find({"bus_id": bus_id}).sort("timestamp", -1).limit(10))

    return [convert_id(item) for item in data]