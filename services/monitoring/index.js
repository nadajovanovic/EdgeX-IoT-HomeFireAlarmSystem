import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import mqtt from "mqtt";


let client;
let currentValue = "ENABLED";

(async () => {
  client = mqtt.connect(`mqtt://broker.hivemq.com`);
  console.log("success");
})().catch((error) => {
  console.log("caught", error.message);
});

const app = express();
app.use(express.json());
app.use(cors());

client.on("connect", function () {
  try {
    client.subscribe("notification");
    console.log("subscribed");
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
    "http://127.0.0.1:59882/api/v2/device/name/Fishpond-Device/temp_reg";
  try {
    const res = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({  "temp_reg": command }),
    });
    console.log(res.status);
  } catch (error) {
    console.log("error", error);
  }
}

client.on("error", function (err) {
  console.log("error", err);
  client.end();
});

app.post("/", (req, res)=> {
  console.log(req.body)

})

app.listen(1234, () => {
  console.log("Server is listening on port 1234.");
});
