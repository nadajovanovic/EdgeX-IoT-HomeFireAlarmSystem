import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import time
import json
import os

load_dotenv()

BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
TOPIC = os.getenv('TOPIC')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD')
DBURL = os.getenv('INFLUX_URL')
TOKEN = os.getenv('INFLUX_TOKEN')
ORG = os.getenv('INFLUX_ORG')
BUCKET = os.getenv('INFLUX_BUCKET')

print("adresa: ",BROKER_ADDRESS)
print("adresa influx: ",DBURL)

def influxDBconnect():
    influxDBConnection = InfluxDBClient(url = DBURL, token=TOKEN, org=ORG)
    return influxDBConnection

def influxDBwrite(device, sensorName, sensorValue):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    write_api = influxDBConnection.write_api(write_options=SYNCHRONOUS)
    p = Point('SmokeDetector').tag("gateway", device).time(timestamp).field(sensorName, sensorValue)
    write_api.write(bucket=BUCKET, org=ORG, record=p)
    
def on_message(client, userdata, message):
    payload = message.payload.decode()
    message = json.loads(payload)
    
    print(message)

    for entry in message["readings"]:
        device = entry["deviceName"]
        sensorName = entry["resourceName"]
        sensorValue = float(entry["value"])
        influxDBwrite(device, sensorName, sensorValue)

influxDBConnection = influxDBconnect()

print("Creating new instance ...")

#Creating new instance
client = mqtt.Client("sub visualization")

#Attach fuction to callback
client.on_message=on_message 

#Connect to broker
print("Connecting to broker ...")
client.connect(BROKER_ADDRESS, 1883)
print("...done")

client.loop_start()

while True:
    client.subscribe(TOPIC)
    time.sleep(1)

