import express from "express";
import cors from "cors";
import mqtt from "mqtt";


let client;
let currentValue = "ENABLE";

(async () => {
  client = mqtt.connect({
    host: "edgex-mqtt-broker",
    port: 1883,
    protocol: "mqtt",
    protocolVersion: 4,
  });
  console.log("Successfully connected to MQTT!");
})().catch((error) => {
  console.log("caught", error.message);
});

const app = express();
app.use(express.json());
app.use(cors());

client.on("connect", function () {
  try {
    client.subscribe("Notifications");
    console.log("Subscribed topic 'Notifications'");
  } catch (err) {
    console.log("err subscribe", err);
  }
});

client.on("message", function (topic, message) {

  console.log(message.toString());
  const m = message.toString();

  if(m!=currentValue){
    if(m == "ENABLED"){
      sendAlert("true")
    }else{
      sendAlert("false")
    }
    currentValue = m;
  }

  //const mes = JSON.parse(message);
  //console.log(message)

  // const device = mes["profileName"]

  // if (device == "Fishpond-Device-Profile"){
  
  //   mes["readings"].forEach(entry => {
     
  //         const resourceName  = entry["resourceName"]
  //         const sensorValue = parseFloat(entry["value"])
  //         console.log(`${resourceName} is ${sensorValue}`);
  //         if(resourceName == "water_temp" && sensorValue > 24){
  //           sendAlert("true")
  //         }
  //         else{
  //           sendAlert("false")
  //         }
      
  //   });      
  //}


});

async function sendAlert(command) {
  const url =
    "http://edgex-core-command:59882/api/v2/device/name/SmokeDetector/FireAlarm";
  try {
    const res = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({  "FireAlarm": command }),
    });
    console.log(res.status);
  } catch (error) {
    console.log("error", error);
  }
}

client.on("error", function (err) {
  console.log("ERROR client on:", err);
  client.end();
});


app.listen(8080, () => {
  console.log("Server is listening on port 8080.");
});
