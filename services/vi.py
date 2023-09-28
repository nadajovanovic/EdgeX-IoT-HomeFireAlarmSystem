import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv
import time
import json
import os

load_dotenv()
broker_address = 'broker.hivemq.com'
topic = 'SmokeDetectorEvents'
dburl = "127.0.0.1:8086"
dbhost = "127.0.0.1"
dbuser = os.getenv('dbuser')
dbpassword = os.getenv('dbpassword')
token = os.getenv('token')
org = os.getenv('org')
bucket = os.getenv('bucket')

def influxDBconnect():
    influxDBConnection = InfluxDBClient(url = dburl, token=token, org=org)
    return influxDBConnection

def influxDBwrite(device, sensorName, sensorValue):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    write_api = influxDBConnection.write_api(write_options=SYNCHRONOUS)
    p = Point('SmokeDetector').tag("gateway", device).time(timestamp).field(sensorName, sensorValue)
    write_api.write(bucket=bucket, org=org, record=p)
    
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
client = mqtt.Client("sub1")

#Attach fuction to callback
client.on_message=on_message 

#Connect to broker
print("Connecting to broker ...")
client.connect(broker_address, 1883)
print("...done")

client.loop_start()

while True:
    client.subscribe(topic)
    time.sleep(1)

