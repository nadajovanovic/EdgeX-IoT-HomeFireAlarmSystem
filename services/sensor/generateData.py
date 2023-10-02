import csv
import requests
import json
import time
import uuid


edgexip = '127.0.0.1'

if __name__ == "__main__":

    csv_file_path = './smoke_detection_iot.csv'

    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            # Generate a unique ID for each event
            event_id = str(uuid.uuid4())
            
            # Generate a Unix timestamp
            event_origin = int(time.time() * 1e9)
            
            # Extract values from the CSV row
            temp = float(row['Temperature[C]'])
            humidity = float(row['Humidity[%]'])
            tvoc = int(row['TVOC[ppb]'])
            eco2 = int(row['eCO2[ppm]'])
            h2 = int(row['Raw H2'])
            ethanol = int(row['Raw Ethanol'])
            pressure = float(row['Pressure[hPa]'])
                          
            # Create the event JSON structure
            event = {
                "apiVersion": "v2",
                "event": {
                    "apiVersion": "v2",
                    "deviceName": "SmokeDetector",
                    "profileName": "SmokeDetector-Device-Profile",
                    "sourceName": "Reading",
                    "id": event_id,
                    "origin": event_origin,
                    "readings": [
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "Temperature",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Float32",
                            "value": str(temp)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "Humidity",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Float32",
                            "value": str(humidity)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "TVOC",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Int32",
                            "value": str(tvoc)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "eCO2",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Int32",
                            "value":str(eco2)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "RawH2",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Int32",
                            "value": str(h2)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "RawEthanol",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Int32",
                            "value": str(ethanol)
                        },
                        {
                            "origin": event_origin,
                            "deviceName": "SmokeDetector",
                            "resourceName": "Pressure",
                            "profileName": "SmokeDetector-Device-Profile",
                            "valueType": "Float32",
                            "value": str(pressure)
                        }
                    ]
                }
            }            

            url = 'http://%s:59880/api/v2/event/SmokeDetector-Device-Profile/SmokeDetector/Reading' % edgexip
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(event), headers=headers, verify=False)
            print(response)
            # print(event)
            time.sleep(10)

