require("dotenv").config();

const mqtt = require('mqtt');
const { InfluxDB, Point } = require('@influxdata/influxdb-client');

const BROKER_ADDRESS = process.env.BROKER_ADDRESS;
const TOPIC = process.env.TOPIC;
const url = process.env.INFLUX_URL;
const token = process.env.INFLUX_TOKEN;
const org = process.env.INFLUX_ORG;
const bucket = process.env.INFLUX_BUCKET;


// Establish InfluxDB connection
const influxDBConnection = influxDBConnect();

console.log("Creating new instance ...");

let client;

(async () => {
    try{
    client = mqtt.connect({
      host: "edgex-mqtt-broker",
      port: 1883,
      protocol: "mqtt",
      protocolVersion: 4,
    });
    console.log("Successfully connected to MQTT!");
}catch(error){
    console.log(error);
    }
  })();


client.on("connect", function () {
    try {
        client.subscribe(TOPIC);
        console.log("Subscribed topic ", TOPIC);
    } catch (err) {
        console.log("err subscribe", err);
    }
});

client.on('message', onMessage);

function onMessage(topic, payload) {

    payload = payload.toString();
    const message = JSON.parse(payload);

    console.log(message);

    for (const entry of message["readings"]) {
        const device = entry["deviceName"];
        const sensorName = entry["resourceName"];
        const sensorValue = parseFloat(entry["value"]);
        influxDBWrite(device, sensorName, sensorValue);
    }
}

client.on("error", function (err) {
    console.log("ERROR client on:", err);
    client.end();
  });

function influxDBConnect() {
    const influxDBConnection = new InfluxDB({url, token});
    return influxDBConnection;
}

function influxDBWrite(device, sensorName, sensorValue) {
    const timestamp = new Date().toISOString();
    const writeApi = influxDBConnection.getWriteApi(org, bucket);
    const point = new Point('SmokeDetector');
    point.timestamp = timestamp;
    point.tag("gateway", device)
    point.floatField(sensorName, sensorValue);

    writeApi.writePoint(point);
    writeApi.close();
}
